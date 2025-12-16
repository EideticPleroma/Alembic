# System Overview

## Vision

Alembic is a Hermetic AI-powered tarot reading application that serves as a digital vessel of transformation. Users engage with tarot not for fortune-telling, but for psychological insight and self-reflection, guided by principles of Hermetic philosophy and depth psychology.

## Architecture Diagram

```mermaid
flowchart TB
    subgraph client [Client Layer]
        Browser[Web Browser]
        NextJS[Next.js 15 App]
        ShadcnUI[shadcn/ui Components]
    end

    subgraph api [API Layer]
        FastAPI[FastAPI Backend]
        Routers[API Routers]
        Services[Service Layer]
    end

    subgraph core [Core Domain]
        Tarot[Tarot Engine]
        LLM[LLM Integration]
        Subscription[Subscription Service]
    end

    subgraph external [External Services]
        Grok[xAI Grok API]
        Supabase[(Supabase)]
        Stripe[Stripe]
    end

    Browser --> NextJS
    NextJS --> ShadcnUI
    NextJS --> FastAPI
    FastAPI --> Routers
    Routers --> Services
    Services --> Tarot
    Services --> LLM
    Services --> Subscription
    LLM --> Grok
    Services --> Supabase
    Subscription --> Stripe
    NextJS -.-> Supabase
```

## Component Responsibilities

### Frontend (Next.js 15)

| Component | Responsibility |
|-----------|---------------|
| `app/page.tsx` | Landing page with marketing content |
| `app/reading/page.tsx` | Main reading interface |
| `app/history/page.tsx` | User's reading history |
| `app/pricing/page.tsx` | Subscription tiers and checkout |
| `components/tarot/` | Card display, spread layouts, animations |
| `components/ui/` | shadcn/ui base components |
| `lib/api.ts` | Backend API client |
| `lib/supabase.ts` | Supabase client for auth |

### Backend (FastAPI)

| Component | Responsibility |
|-----------|---------------|
| `app/main.py` | Application entry point, middleware |
| `app/api/routers/reading.py` | Reading creation and retrieval endpoints |
| `app/api/routers/chat.py` | Follow-up conversation endpoints |
| `app/api/routers/user.py` | User profile and data export |
| `app/api/routers/webhook.py` | Stripe webhook handlers |
| `app/core/tarot/` | Deck, cards, spreads business logic |
| `app/core/llm/` | Grok integration and prompt management |
| `app/core/services/` | Business logic orchestration |

### External Services

| Service | Purpose | Integration |
|---------|---------|-------------|
| **Supabase** | Auth, database, storage | Direct from frontend (auth), via backend (data) |
| **xAI Grok** | LLM interpretations | Via LiteLLM in backend |
| **Stripe** | Payment processing | Checkout from frontend, webhooks to backend |

## Data Flow

### Reading Creation Flow

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Frontend
    participant API as Backend
    participant DB as Supabase
    participant LLM as Grok

    U->>FE: Enter question, select spread
    FE->>API: POST /api/reading
    API->>API: Validate user credits/subscription
    API->>API: Draw cards (crypto random)
    API->>LLM: Generate interpretation
    LLM-->>API: Interpretation text
    API->>DB: Store reading
    DB-->>API: Reading ID
    API-->>FE: Reading response
    FE-->>U: Animated card reveal + interpretation
```

### Authentication Flow

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Frontend
    participant SB as Supabase Auth
    participant API as Backend

    U->>FE: Click login
    FE->>SB: Redirect to auth
    SB-->>FE: Return JWT
    FE->>FE: Store JWT
    FE->>API: Request with JWT
    API->>SB: Validate JWT
    SB-->>API: User info
    API-->>FE: Authorized response
```

### Payment Flow

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Frontend
    participant API as Backend
    participant ST as Stripe
    participant DB as Supabase

    U->>FE: Select subscription
    FE->>API: POST /api/checkout
    API->>ST: Create checkout session
    ST-->>API: Session URL
    API-->>FE: Redirect URL
    FE->>ST: Redirect to checkout
    U->>ST: Complete payment
    ST->>API: Webhook: checkout.session.completed
    API->>DB: Update subscription status
    ST-->>FE: Redirect to success page
```

## Security Architecture

### Authentication

- **Provider**: Supabase Auth
- **Method**: JWT tokens
- **Session**: Refresh token rotation
- **MFA**: Optional for users

### Authorization

- **Row Level Security**: All database tables
- **Ownership checks**: Backend verifies user owns resources
- **Rate limiting**: Per-endpoint limits

### Data Protection

- **Encryption at rest**: Supabase default
- **Encryption in transit**: HTTPS everywhere
- **Secrets**: Environment variables only
- **Payment data**: Never touches our servers (Stripe Elements)

## Scalability Considerations

### Current Architecture (MVP)

- Single Vercel deployment (auto-scaling)
- Single Railway instance (can scale vertically)
- Supabase managed PostgreSQL (connection pooling)
- Grok API (rate limited by provider)

### Future Scaling

- **Database**: Read replicas if needed
- **Caching**: Redis for session/response caching
- **CDN**: Vercel Edge for static assets
- **LLM**: Response caching for common patterns

## Monitoring

- **Error tracking**: Sentry
- **Uptime**: External monitoring service
- **Logs**: Structured JSON, Railway log aggregation
- **Metrics**: Custom dashboards for business metrics

## Disaster Recovery

- **Database backups**: Supabase automatic daily
- **Code**: Git repository (GitHub)
- **Secrets**: Documented in secure location
- **Recovery time**: < 1 hour for full restoration

