# Local Development Guide

## Prerequisites

- **Node.js** 20+ (for frontend)
- **Python** 3.11+ (for backend)
- **Docker** (optional, for local Ollama)
- **Git**

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/alembic.git
cd alembic

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run database migrations (after Supabase setup)
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Local LLM (Optional)

For free local development without API costs:

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama3.2

# Ollama runs automatically on localhost:11434
```

## Environment Variables

### Backend (`backend/.env`)

```bash
# Required
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# LLM (one of these)
XAI_API_KEY=xai-xxx  # For Grok
# Or leave empty to use local Ollama

# Stripe (for payment testing)
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# Optional
LOG_LEVEL=DEBUG
CORS_ORIGINS=http://localhost:3000
```

### Frontend (`frontend/.env.local`)

```bash
# Required
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=http://localhost:8000

# Stripe (for checkout)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_xxx
```

## Supabase Setup

### 1. Create Project

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Note your project URL and keys

### 2. Run Migrations

```sql
-- Run these in Supabase SQL Editor

-- Users table (extends auth.users)
CREATE TABLE users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    tier TEXT NOT NULL DEFAULT 'free',
    credits INTEGER NOT NULL DEFAULT 3,
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
ON users FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
ON users FOR UPDATE USING (auth.uid() = id);

-- Readings table
CREATE TABLE readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    spread_type TEXT NOT NULL,
    cards JSONB NOT NULL,
    interpretation TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE readings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own readings"
ON readings FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own readings"
ON readings FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Add more tables as needed (see data-model.md)
```

### 3. Configure Auth

1. Go to Authentication > Providers
2. Enable Email provider
3. Optionally enable Google, GitHub, etc.

## Development Workflow

### Running Both Services

Terminal 1 (Backend):
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

### Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Linting

```bash
# Backend
cd backend
ruff check .
mypy .

# Frontend
cd frontend
npm run lint
npm run type-check
```

## Common Tasks

### Add a New API Endpoint

1. Create router in `backend/app/api/routers/`
2. Add schema in `backend/app/schemas/`
3. Add service logic in `backend/app/core/services/`
4. Register router in `backend/app/main.py`
5. Add tests in `backend/tests/`

### Add a New UI Component

1. Install shadcn component: `npx shadcn-ui@latest add <component>`
2. Create wrapper in `frontend/src/components/`
3. Use in pages

### Add a New Database Table

1. Create migration: `alembic revision --autogenerate -m "add_table"`
2. Review and edit migration file
3. Apply: `alembic upgrade head`
4. Add model in `backend/app/models/`
5. Add schema in `backend/app/schemas/`

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :8000  # or :3000

# Kill it
kill -9 <PID>
```

### Supabase Connection Issues

1. Check your `.env` file has correct keys
2. Verify project is running in Supabase dashboard
3. Check network connectivity

### Ollama Not Responding

```bash
# Check if running
curl http://localhost:11434/api/tags

# Restart
ollama serve
```

### Frontend Can't Reach Backend

1. Verify backend is running on port 8000
2. Check CORS_ORIGINS in backend `.env`
3. Check NEXT_PUBLIC_API_URL in frontend `.env.local`

## IDE Setup

### VS Code / Cursor

Recommended extensions:
- Python
- Pylance
- ESLint
- Tailwind CSS IntelliSense
- Prettier

Settings (`.vscode/settings.json`):
```json
{
  "python.defaultInterpreterPath": "./backend/.venv/bin/python",
  "editor.formatOnSave": true,
  "python.formatting.provider": "black",
  "typescript.preferences.importModuleSpecifier": "relative"
}
```

## Next Steps

- [Deployment Guide](./deployment.md)
- [Stripe Setup Guide](./stripe-setup.md)
- [Architecture Overview](../architecture/system-overview.md)

