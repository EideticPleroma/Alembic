# Deployment Guide

## Overview

Alembic is deployed as two services:
- **Frontend**: Vercel (Next.js)
- **Backend**: Railway (FastAPI)
- **Database**: Supabase (managed PostgreSQL)

## Prerequisites

- GitHub repository with your code
- Vercel account
- Railway account
- Supabase project (already set up)
- Stripe account (for payments)
- Domain name (optional but recommended)

## Backend Deployment (Railway)

### 1. Prepare Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Copy application
COPY app/ app/

# Run with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project" > "Deploy from GitHub repo"
3. Select your repository
4. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: (auto-detected from Dockerfile)
   - **Start Command**: (auto-detected from Dockerfile)

### 3. Configure Environment Variables

In Railway dashboard, add:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
XAI_API_KEY=xai-xxx
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
CORS_ORIGINS=https://alembic.app,https://www.alembic.app
LOG_LEVEL=INFO
```

### 4. Set Up Custom Domain (Optional)

1. In Railway, go to Settings > Domains
2. Add custom domain: `api.alembic.app`
3. Configure DNS with your registrar

### 5. Verify Deployment

```bash
curl https://api.alembic.app/health
```

## Frontend Deployment (Vercel)

### 1. Connect to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New" > "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`

### 2. Configure Environment Variables

In Vercel dashboard, add:

```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=https://api.alembic.app
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxx
```

### 3. Set Up Custom Domain

1. In Vercel, go to Settings > Domains
2. Add: `alembic.app` and `www.alembic.app`
3. Configure DNS:
   ```
   A     @     76.76.21.21
   CNAME www   cname.vercel-dns.com
   ```

### 4. Verify Deployment

Visit `https://alembic.app`

## Database Setup (Production)

### 1. Supabase Production Settings

1. Go to Supabase Dashboard > Settings
2. Under "General":
   - Ensure project is in production mode
   - Enable Point-in-Time Recovery (Pro plan)
3. Under "Auth":
   - Configure site URL: `https://alembic.app`
   - Add redirect URLs

### 2. Run Production Migrations

```bash
# Connect to production database
export DATABASE_URL="postgresql://..."

# Run migrations
cd backend
alembic upgrade head
```

### 3. Enable Row Level Security

Verify all tables have RLS enabled:

```sql
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public';
```

## Stripe Production Setup

### 1. Activate Live Mode

1. Go to Stripe Dashboard
2. Toggle to "Live mode"
3. Complete business verification

### 2. Create Products

```
Products:
- Seeker Monthly: $7/month
- Initiate Monthly: $15/month
- Credit Pack (20): $5 one-time
```

### 3. Configure Webhooks

1. Go to Developers > Webhooks
2. Add endpoint: `https://api.alembic.app/api/webhook/stripe`
3. Select events:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_failed`
4. Note the webhook signing secret

### 4. Update Environment Variables

Update Railway with live Stripe keys:
```
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

## SSL/TLS

Both Vercel and Railway provide automatic SSL certificates. Verify:

```bash
curl -I https://alembic.app
curl -I https://api.alembic.app
```

Should show `HTTP/2 200` with valid certificates.

## Monitoring Setup

### Sentry

1. Create project at [sentry.io](https://sentry.io)
2. Add DSN to environment variables:
   ```
   # Backend
   SENTRY_DSN=https://xxx@sentry.io/xxx
   
   # Frontend
   NEXT_PUBLIC_SENTRY_DSN=https://xxx@sentry.io/xxx
   ```

### Uptime Monitoring

Set up external monitoring (e.g., UptimeRobot, Better Uptime):
- Monitor: `https://alembic.app`
- Monitor: `https://api.alembic.app/health`
- Alert on downtime

## CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Test Backend
        run: |
          cd backend
          pip install -e ".[dev]"
          pytest
      
      - name: Test Frontend
        run: |
          cd frontend
          npm ci
          npm test

  # Vercel and Railway auto-deploy from main branch
```

## Rollback Procedures

### Vercel Rollback

1. Go to Vercel Dashboard > Deployments
2. Find previous working deployment
3. Click "..." > "Promote to Production"

### Railway Rollback

1. Go to Railway Dashboard > Deployments
2. Find previous working deployment
3. Click "Redeploy"

### Database Rollback

```bash
# Rollback last migration
alembic downgrade -1

# Or to specific version
alembic downgrade <revision_id>
```

## Checklist

Before going live:

- [ ] All environment variables set in production
- [ ] Database migrations applied
- [ ] RLS enabled on all tables
- [ ] SSL working on all domains
- [ ] Stripe webhooks configured
- [ ] Error tracking configured
- [ ] Uptime monitoring configured
- [ ] Backup strategy verified
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Legal pages published (privacy, terms)

