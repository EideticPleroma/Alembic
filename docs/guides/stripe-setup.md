# Stripe Setup Guide

## Overview

Alembic uses Stripe for:
- Monthly subscriptions (Seeker, Initiate tiers)
- One-time credit purchases
- Customer management
- Webhook handling

## Initial Setup

### 1. Create Stripe Account

1. Go to [stripe.com](https://stripe.com)
2. Create an account
3. Complete business verification (required for live payments)

### 2. Get API Keys

1. Go to Developers > API Keys
2. Note your keys:
   - **Publishable key** (pk_test_xxx) - for frontend
   - **Secret key** (sk_test_xxx) - for backend

## Product Configuration

### Create Products

In Stripe Dashboard > Products:

#### Seeker Subscription

```
Name: Seeker
Description: Unlimited tarot readings with follow-up conversations
Price:
  - $7.00 USD / month
  - Recurring
  - ID: price_seeker_monthly
```

#### Initiate Subscription

```
Name: Initiate
Description: Full access with unlimited history and export
Price:
  - $15.00 USD / month
  - Recurring
  - ID: price_initiate_monthly
```

#### Credit Pack

```
Name: Reading Credits (20 pack)
Description: 20 tarot reading credits
Price:
  - $5.00 USD (one-time)
  - ID: price_credits_20
```

### Note Price IDs

After creating, note the price IDs for use in code:
```
price_seeker_monthly: price_xxx
price_initiate_monthly: price_xxx
price_credits_20: price_xxx
```

## Backend Integration

### Install Stripe SDK

```bash
pip install stripe
```

### Configuration

```python
# backend/app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    stripe_secret_key: str
    stripe_webhook_secret: str
    stripe_price_seeker: str = "price_xxx"
    stripe_price_initiate: str = "price_xxx"
    stripe_price_credits: str = "price_xxx"
```

### Checkout Session Creation

```python
# backend/app/api/routers/checkout.py
import stripe
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/checkout", tags=["checkout"])

@router.post("/subscription")
async def create_subscription_checkout(
    price_id: str,
    user: User = Depends(get_current_user),
):
    stripe.api_key = settings.stripe_secret_key
    
    try:
        # Get or create Stripe customer
        customer = await get_or_create_customer(user)
        
        session = stripe.checkout.Session.create(
            customer=customer.id,
            mode="subscription",
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            success_url=f"{settings.frontend_url}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.frontend_url}/pricing",
            metadata={"user_id": str(user.id)},
        )
        
        return {"checkout_url": session.url}
        
    except stripe.error.StripeError as e:
        raise HTTPException(400, str(e))


@router.post("/credits")
async def create_credits_checkout(
    user: User = Depends(get_current_user),
):
    stripe.api_key = settings.stripe_secret_key
    
    try:
        customer = await get_or_create_customer(user)
        
        session = stripe.checkout.Session.create(
            customer=customer.id,
            mode="payment",
            payment_method_types=["card"],
            line_items=[{"price": settings.stripe_price_credits, "quantity": 1}],
            success_url=f"{settings.frontend_url}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.frontend_url}/pricing",
            metadata={
                "user_id": str(user.id),
                "credits": "20",
            },
        )
        
        return {"checkout_url": session.url}
        
    except stripe.error.StripeError as e:
        raise HTTPException(400, str(e))
```

### Webhook Handler

```python
# backend/app/api/routers/webhook.py
import stripe
from fastapi import APIRouter, Request, HTTPException

router = APIRouter(prefix="/webhook", tags=["webhook"])

@router.post("/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except ValueError:
        raise HTTPException(400, "Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(400, "Invalid signature")
    
    # Handle events
    if event.type == "checkout.session.completed":
        session = event.data.object
        await handle_checkout_completed(session)
        
    elif event.type == "customer.subscription.updated":
        subscription = event.data.object
        await handle_subscription_updated(subscription)
        
    elif event.type == "customer.subscription.deleted":
        subscription = event.data.object
        await handle_subscription_deleted(subscription)
        
    elif event.type == "invoice.payment_failed":
        invoice = event.data.object
        await handle_payment_failed(invoice)
    
    return {"status": "ok"}


async def handle_checkout_completed(session):
    """Process successful checkout."""
    user_id = session.metadata.get("user_id")
    
    if session.mode == "subscription":
        # Update user tier based on subscription
        subscription = stripe.Subscription.retrieve(session.subscription)
        price_id = subscription.items.data[0].price.id
        
        if price_id == settings.stripe_price_seeker:
            tier = "seeker"
        elif price_id == settings.stripe_price_initiate:
            tier = "initiate"
        else:
            tier = "free"
        
        await update_user_tier(user_id, tier, subscription.id)
        
    elif session.mode == "payment":
        # Add credits
        credits = int(session.metadata.get("credits", 0))
        await add_user_credits(user_id, credits)


async def handle_subscription_updated(subscription):
    """Handle subscription changes."""
    customer_id = subscription.customer
    user = await get_user_by_stripe_customer(customer_id)
    
    if subscription.status == "active":
        # Update tier
        price_id = subscription.items.data[0].price.id
        tier = "seeker" if price_id == settings.stripe_price_seeker else "initiate"
        await update_user_tier(user.id, tier)
    else:
        # Downgrade to free
        await update_user_tier(user.id, "free")


async def handle_subscription_deleted(subscription):
    """Handle cancellation."""
    customer_id = subscription.customer
    user = await get_user_by_stripe_customer(customer_id)
    await update_user_tier(user.id, "free")


async def handle_payment_failed(invoice):
    """Handle failed payment."""
    customer_id = invoice.customer
    user = await get_user_by_stripe_customer(customer_id)
    # Send notification, consider grace period
    await notify_payment_failed(user)
```

## Frontend Integration

### Install Stripe

```bash
npm install @stripe/stripe-js @stripe/react-stripe-js
```

### Stripe Provider

```typescript
// frontend/src/lib/stripe.ts
import { loadStripe } from '@stripe/stripe-js';

export const stripePromise = loadStripe(
  process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!
);
```

### Pricing Page

```typescript
// frontend/src/app/pricing/page.tsx
"use client";

import { useState } from 'react';

const plans = [
  {
    name: 'Seeker',
    price: '$7',
    priceId: 'price_seeker_monthly',
    features: ['Unlimited readings', 'All spreads', 'Follow-up chat'],
  },
  {
    name: 'Initiate',
    price: '$15',
    priceId: 'price_initiate_monthly',
    features: ['Everything in Seeker', 'Unlimited history', 'Export readings'],
  },
];

export default function PricingPage() {
  const [loading, setLoading] = useState<string | null>(null);

  const handleSubscribe = async (priceId: string) => {
    setLoading(priceId);
    
    const response = await fetch('/api/checkout/subscription', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ price_id: priceId }),
    });
    
    const { checkout_url } = await response.json();
    window.location.href = checkout_url;
  };

  return (
    <div className="grid grid-cols-2 gap-8">
      {plans.map((plan) => (
        <div key={plan.name} className="p-6 border rounded-lg">
          <h2 className="text-2xl font-bold">{plan.name}</h2>
          <p className="text-3xl">{plan.price}/mo</p>
          <ul>
            {plan.features.map((f) => (
              <li key={f}>{f}</li>
            ))}
          </ul>
          <button
            onClick={() => handleSubscribe(plan.priceId)}
            disabled={loading === plan.priceId}
          >
            {loading === plan.priceId ? 'Loading...' : 'Subscribe'}
          </button>
        </div>
      ))}
    </div>
  );
}
```

## Webhook Testing

### Local Testing with Stripe CLI

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:8000/api/webhook/stripe

# Note the webhook signing secret (whsec_xxx)
# Add to backend/.env as STRIPE_WEBHOOK_SECRET
```

### Test Events

```bash
# Trigger test checkout
stripe trigger checkout.session.completed

# Trigger subscription events
stripe trigger customer.subscription.created
stripe trigger customer.subscription.updated
stripe trigger customer.subscription.deleted
```

## Going Live

### 1. Complete Stripe Verification

- Business verification
- Bank account connection
- Identity verification

### 2. Switch to Live Keys

```bash
# Backend
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx  # New webhook secret for live

# Frontend
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxx
```

### 3. Create Live Webhook

1. Stripe Dashboard > Webhooks
2. Add endpoint: `https://api.alembic.app/api/webhook/stripe`
3. Select events
4. Note new signing secret

### 4. Test Live Flow

Make a real $1 test purchase to verify everything works.

## Troubleshooting

### Webhook Signature Errors

- Verify webhook secret matches
- Ensure raw body is passed (not parsed JSON)
- Check for middleware that modifies request body

### Customer Not Found

- Verify customer is created before checkout
- Check metadata is passed correctly

### Subscription Not Updating

- Check webhook events are being received
- Verify event handling logic
- Check database updates are successful

