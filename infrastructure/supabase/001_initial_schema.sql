-- ============================================
-- ALEMBIC DATABASE SCHEMA
-- Run this in Supabase SQL Editor
-- ============================================

-- ============================================
-- 1. HELPER FUNCTIONS
-- ============================================

-- Helper function for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- 2. USERS TABLE
-- ============================================

CREATE TABLE users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    tier TEXT NOT NULL DEFAULT 'free' CHECK (tier IN ('free', 'seeker', 'initiate')),
    credits INTEGER NOT NULL DEFAULT 3,
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users can view own profile"
ON users FOR SELECT
USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
ON users FOR UPDATE
USING (auth.uid() = id);

-- Trigger for updated_at
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 3. READINGS TABLE
-- ============================================

CREATE TABLE readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    spread_type TEXT NOT NULL CHECK (spread_type IN ('single', 'three_card', 'shadow_work', 'celtic_cross')),
    cards JSONB NOT NULL,
    interpretation TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_readings_user_id ON readings(user_id);
CREATE INDEX idx_readings_created_at ON readings(created_at DESC);

-- Enable RLS
ALTER TABLE readings ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users can view own readings"
ON readings FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can create own readings"
ON readings FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own readings"
ON readings FOR DELETE
USING (auth.uid() = user_id);

-- ============================================
-- 4. READING MESSAGES TABLE (for follow-up chat)
-- ============================================

CREATE TABLE reading_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reading_id UUID NOT NULL REFERENCES readings(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_reading_messages_reading_id ON reading_messages(reading_id);

-- Enable RLS
ALTER TABLE reading_messages ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users can view messages for own readings"
ON reading_messages FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM readings
        WHERE readings.id = reading_messages.reading_id
        AND readings.user_id = auth.uid()
    )
);

CREATE POLICY "Users can create messages for own readings"
ON reading_messages FOR INSERT
WITH CHECK (
    EXISTS (
        SELECT 1 FROM readings
        WHERE readings.id = reading_messages.reading_id
        AND readings.user_id = auth.uid()
    )
);

-- ============================================
-- 5. SUBSCRIPTIONS TABLE (for Stripe)
-- ============================================

CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    stripe_customer_id TEXT NOT NULL,
    stripe_subscription_id TEXT,
    status TEXT NOT NULL DEFAULT 'inactive' 
        CHECK (status IN ('active', 'canceled', 'past_due', 'inactive')),
    plan TEXT CHECK (plan IN ('seeker', 'initiate')),
    current_period_end TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE UNIQUE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_stripe_customer_id ON subscriptions(stripe_customer_id);

-- Enable RLS
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users can view own subscription"
ON subscriptions FOR SELECT
USING (auth.uid() = user_id);

-- Trigger
CREATE TRIGGER update_subscriptions_updated_at
    BEFORE UPDATE ON subscriptions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 6. CREDIT TRANSACTIONS TABLE (audit log)
-- ============================================

CREATE TABLE credit_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount INTEGER NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('purchase', 'usage', 'refund', 'bonus')),
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_credit_transactions_user_id ON credit_transactions(user_id);

-- Enable RLS
ALTER TABLE credit_transactions ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users can view own transactions"
ON credit_transactions FOR SELECT
USING (auth.uid() = user_id);

-- ============================================
-- 7. HELPER FUNCTION: Deduct Credits
-- ============================================

CREATE OR REPLACE FUNCTION deduct_credits(
    p_user_id UUID,
    p_amount INTEGER,
    p_description TEXT
) RETURNS BOOLEAN AS $$
DECLARE
    v_current_credits INTEGER;
BEGIN
    -- Get current credits with lock
    SELECT credits INTO v_current_credits
    FROM users
    WHERE id = p_user_id
    FOR UPDATE;
    
    -- Check sufficient credits
    IF v_current_credits < p_amount THEN
        RETURN FALSE;
    END IF;
    
    -- Deduct credits
    UPDATE users
    SET credits = credits - p_amount
    WHERE id = p_user_id;
    
    -- Log transaction
    INSERT INTO credit_transactions (user_id, amount, type, description)
    VALUES (p_user_id, -p_amount, 'usage', p_description);
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================
-- 7. LLM USAGE TABLE (ops tracking for cost analysis)
-- ============================================

CREATE TABLE llm_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    reading_id UUID REFERENCES readings(id) ON DELETE SET NULL,
    model TEXT NOT NULL,
    provider TEXT NOT NULL,
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL,
    total_tokens INTEGER NOT NULL,
    cost_usd NUMERIC(10, 6) NOT NULL,
    latency_ms INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for efficient querying
CREATE INDEX idx_llm_usage_user_id ON llm_usage(user_id);
CREATE INDEX idx_llm_usage_reading_id ON llm_usage(reading_id);
CREATE INDEX idx_llm_usage_created_at ON llm_usage(created_at DESC);
CREATE INDEX idx_llm_usage_model ON llm_usage(model);
CREATE INDEX idx_llm_usage_provider ON llm_usage(provider);

-- Enable RLS
ALTER TABLE llm_usage ENABLE ROW LEVEL SECURITY;

-- Policies: Admin-only access (service role for inserts, no user access to raw data)
-- Service role can insert usage records
-- (INSERT is allowed via service role without explicit policy)

-- Prevent users from querying raw llm_usage (ops data only)
CREATE POLICY "Disable user access to llm_usage"
ON llm_usage FOR SELECT
USING (FALSE);

-- ============================================
-- 8. TRIGGER: Auto-create user profile on signup
-- ============================================

CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.users (id, email)
    VALUES (NEW.id, NEW.email);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger on auth.users
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION handle_new_user();

-- ============================================
-- VERIFICATION QUERY
-- Run this to verify all tables were created:
-- ============================================
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

