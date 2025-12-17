# Project Tasks

## Active Tasks

```dataview
TASK
FROM "02-project"
WHERE !completed
SORT priority DESC
```

## Completed Tasks

```dataview
TASK
FROM "02-project"
WHERE completed
SORT completion DESC
LIMIT 20
```

## By Phase

### Phase 0: Foundation
- [x] Initialize Next.js 15 project #phase0 ✅ 2025-12-17
- [x] Initialize FastAPI project #phase0 ✅ 2025-12-17
- [x] Set up local Ollama #phase0 ✅ 2025-12-17
- [x] Configure environment variables #phase0 ✅ 2025-12-17
- [x] Set up Git repository #phase0 ✅ 2025-12-17

### Phase 1: Core Reading
- [ ] Create 78-card deck data #phase1 #priority-high
- [ ] Implement card draw logic #phase1
- [ ] Build three-card spread #phase1
- [ ] Design Hermetic system prompt #phase1 #priority-high
- [ ] Integrate Grok via LiteLLM #phase1
- [ ] Create reading API endpoint #phase1
- [ ] Build Card component #phase1
- [ ] Build Spread layout #phase1
- [ ] Connect frontend to API #phase1

### Phase 2: Users
- [ ] Configure Supabase Auth #phase2
- [ ] Create user profile table #phase2
- [ ] Create readings table #phase2
- [ ] Build auth UI components #phase2
- [ ] Implement protected routes #phase2
- [ ] Build reading history page #phase2

### Phase 3: Chat
- [ ] Design conversation data model #phase3
- [ ] Create follow-up prompt template #phase3
- [ ] Build chat API endpoint #phase3
- [ ] Create chat UI component #phase3
- [ ] Implement streaming responses #phase3

### Phase 4: Payments
- [ ] Set up Stripe account #phase4
- [ ] Create subscription products #phase4
- [ ] Implement Stripe Checkout #phase4
- [ ] Build webhook handler #phase4
- [ ] Implement usage tracking #phase4
- [ ] Create upgrade prompts #phase4

### Phase 5: Polish
- [ ] Design landing page #phase5
- [ ] Implement SEO metadata #phase5
- [ ] Add error boundaries #phase5
- [ ] Set up Sentry monitoring #phase5
- [ ] Configure production deployment #phase5
- [ ] Write legal pages #phase5

