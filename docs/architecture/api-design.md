# API Design

## Overview

Alembic's API follows RESTful conventions with JSON request/response bodies. All endpoints require authentication except health checks and public documentation.

## Base URL

- **Development**: `http://localhost:8000/api`
- **Production**: `https://api.alembic.app/api`

## Authentication

All protected endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <supabase_jwt>
```

## Endpoints

### Health

#### GET /health

Check API health status.

**Authentication**: None

**Response** `200 OK`:
```json
{
  "status": "healthy",
  "checks": {
    "database": true,
    "llm": true,
    "stripe": true
  },
  "timestamp": "2025-12-16T14:30:00Z"
}
```

---

### Readings

#### POST /api/reading

Create a new tarot reading.

**Authentication**: Required

**Request Body**:
```json
{
  "question": "What should I focus on today?",
  "spread_type": "three_card"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| question | string | Yes | User's question (1-1000 chars) |
| spread_type | string | Yes | One of: `single`, `three_card`, `shadow_work`, `celtic_cross` |

**Response** `201 Created`:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "question": "What should I focus on today?",
  "spread_type": "three_card",
  "cards": [
    {
      "id": "major_0",
      "name": "The Fool",
      "position": "Past",
      "reversed": false,
      "image_url": "/cards/major_0.png"
    },
    {
      "id": "major_1",
      "name": "The Magician",
      "position": "Present",
      "reversed": true,
      "image_url": "/cards/major_1.png"
    },
    {
      "id": "cups_ace",
      "name": "Ace of Cups",
      "position": "Future",
      "reversed": false,
      "image_url": "/cards/cups_ace.png"
    }
  ],
  "interpretation": "The Fool in your Past position speaks to a recent beginning...",
  "created_at": "2025-12-16T14:30:00Z"
}
```

**Errors**:
- `400 Bad Request` - Invalid question or spread type
- `401 Unauthorized` - Missing or invalid token
- `402 Payment Required` - Insufficient credits
- `429 Too Many Requests` - Rate limit exceeded

---

#### GET /api/reading/{reading_id}

Retrieve a specific reading.

**Authentication**: Required

**Response** `200 OK`:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "question": "What should I focus on today?",
  "spread_type": "three_card",
  "cards": [...],
  "interpretation": "...",
  "messages": [
    {
      "role": "assistant",
      "content": "The cards reveal...",
      "created_at": "2025-12-16T14:30:00Z"
    },
    {
      "role": "user",
      "content": "Can you tell me more about The Fool?",
      "created_at": "2025-12-16T14:31:00Z"
    },
    {
      "role": "assistant",
      "content": "The Fool represents...",
      "created_at": "2025-12-16T14:31:30Z"
    }
  ],
  "created_at": "2025-12-16T14:30:00Z"
}
```

**Errors**:
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Reading belongs to another user
- `404 Not Found` - Reading doesn't exist

---

#### GET /api/readings

List user's readings.

**Authentication**: Required

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | integer | 20 | Max results (1-100) |
| offset | integer | 0 | Pagination offset |
| spread_type | string | - | Filter by spread type |

**Response** `200 OK`:
```json
{
  "readings": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "question": "What should I focus on today?",
      "spread_type": "three_card",
      "created_at": "2025-12-16T14:30:00Z"
    }
  ],
  "total": 42,
  "limit": 20,
  "offset": 0
}
```

---

#### DELETE /api/reading/{reading_id}

Delete a reading.

**Authentication**: Required

**Response** `204 No Content`

**Errors**:
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Reading belongs to another user
- `404 Not Found` - Reading doesn't exist

---

### Chat

#### POST /api/reading/{reading_id}/chat

Continue conversation about a reading.

**Authentication**: Required

**Request Body**:
```json
{
  "message": "Can you tell me more about The Fool?"
}
```

**Response** `200 OK`:
```json
{
  "role": "assistant",
  "content": "The Fool in your reading represents...",
  "created_at": "2025-12-16T14:31:30Z"
}
```

**Errors**:
- `400 Bad Request` - Empty message
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Reading belongs to another user
- `404 Not Found` - Reading doesn't exist

---

#### POST /api/reading/{reading_id}/chat/stream

Stream conversation response (Server-Sent Events).

**Authentication**: Required

**Request Body**:
```json
{
  "message": "Can you tell me more about The Fool?"
}
```

**Response** `200 OK` (text/event-stream):
```
data: The
data: Fool
data: in
data: your
data: reading
data: represents
data: ...
data: [DONE]
```

---

### User

#### GET /api/user/profile

Get current user profile.

**Authentication**: Required

**Response** `200 OK`:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "tier": "seeker",
  "credits": 15,
  "preferences": {
    "marketing_emails": false,
    "analytics_tracking": true
  },
  "created_at": "2025-12-01T10:00:00Z"
}
```

---

#### PATCH /api/user/profile

Update user profile.

**Authentication**: Required

**Request Body**:
```json
{
  "preferences": {
    "marketing_emails": true
  }
}
```

**Response** `200 OK`:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "tier": "seeker",
  "credits": 15,
  "preferences": {
    "marketing_emails": true,
    "analytics_tracking": true
  },
  "created_at": "2025-12-01T10:00:00Z"
}
```

---

#### GET /api/user/export

Export all user data (GDPR compliance).

**Authentication**: Required

**Response** `200 OK`:
```json
{
  "profile": {
    "id": "...",
    "email": "...",
    "tier": "...",
    "created_at": "..."
  },
  "readings": [...],
  "subscription": {...},
  "credit_transactions": [...],
  "exported_at": "2025-12-16T14:30:00Z"
}
```

---

#### DELETE /api/user/account

Delete user account and all data.

**Authentication**: Required

**Request Body**:
```json
{
  "confirm_text": "DELETE MY ACCOUNT"
}
```

**Response** `204 No Content`

**Errors**:
- `400 Bad Request` - Confirmation text doesn't match

---

### Checkout

#### POST /api/checkout

Create Stripe checkout session.

**Authentication**: Required

**Request Body**:
```json
{
  "price_id": "price_xxx",
  "success_url": "https://alembic.app/success",
  "cancel_url": "https://alembic.app/pricing"
}
```

**Response** `200 OK`:
```json
{
  "checkout_url": "https://checkout.stripe.com/..."
}
```

---

#### POST /api/checkout/credits

Purchase credits.

**Authentication**: Required

**Request Body**:
```json
{
  "credit_pack": "20",
  "success_url": "https://alembic.app/success",
  "cancel_url": "https://alembic.app/pricing"
}
```

**Response** `200 OK`:
```json
{
  "checkout_url": "https://checkout.stripe.com/..."
}
```

---

### Webhooks

#### POST /api/webhook/stripe

Handle Stripe webhooks.

**Authentication**: Stripe signature verification

**Handled Events**:
- `checkout.session.completed`
- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `invoice.payment_failed`

**Response** `200 OK`

---

## Error Format

All errors follow a consistent format:

```json
{
  "error": "INSUFFICIENT_CREDITS",
  "message": "You've run out of credits. Purchase more to continue.",
  "details": {
    "required": 1,
    "available": 0
  }
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request body |
| `UNAUTHORIZED` | 401 | Missing or invalid auth token |
| `FORBIDDEN` | 403 | No permission for resource |
| `NOT_FOUND` | 404 | Resource doesn't exist |
| `INSUFFICIENT_CREDITS` | 402 | No credits remaining |
| `SUBSCRIPTION_REQUIRED` | 402 | Feature requires subscription |
| `RATE_LIMITED` | 429 | Too many requests |
| `LLM_TIMEOUT` | 503 | LLM request timed out |
| `LLM_ERROR` | 503 | LLM service error |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| POST /api/reading | 10/minute |
| POST /api/reading/{id}/chat | 20/minute |
| POST /api/checkout | 5/minute |
| Other endpoints | 60/minute |

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1702738200
```

## Versioning

The API is currently v1 (implicit in `/api` prefix). Future versions will use:
- `/api/v2/...`

V1 will be maintained for at least 6 months after v2 release.

