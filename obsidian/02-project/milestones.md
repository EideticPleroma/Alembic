# Project Milestones

## Timeline Overview

| Phase | Target Date | Status |
|-------|-------------|--------|
| Phase 0: Foundation | Week 1 | Not Started |
| Phase 1: Core Reading | Weeks 2-3 | Not Started |
| Phase 2: Users | Week 4 | Not Started |
| Phase 3: Chat | Week 5 | Not Started |
| Phase 4: Payments | Week 6 | Not Started |
| Phase 5: Polish | Week 7 | Not Started |
| Launch | Week 8 | Not Started |

---

## Phase 0: Foundation
**Target**: End of Week 1
**Goal**: Development environment ready, project structure established

### Deliverables
- [x] Next.js 15 project initialized with shadcn/ui ✅ 2025-12-16
- [x] FastAPI project initialized with structure ✅ 2025-12-16
- [x] Supabase project created with initial schema ✅ 2025-12-16
- [x] Local Ollama running for free development ✅ 2025-12-16
- [x] Git repository with initial commit ✅ 2025-12-16
- [x] Environment variables documented ✅ 2025-12-16

### Success Criteria
- Can run `npm run dev` and see Next.js app
- Can run `uvicorn app.main:app` and see FastAPI docs
- Can connect to Supabase from both
- Local LLM responds to test prompts

---

## Phase 1: Core Reading
**Target**: End of Week 3
**Goal**: Working three-card reading with Grok interpretation

### Deliverables
- [ ] Complete 78-card deck with meanings
- [ ] Three-card spread implementation
- [ ] Hermetic system prompt refined
- [ ] `/api/reading` endpoint functional
- [ ] Card display with flip animation
- [ ] End-to-end reading flow working

### Success Criteria
- Can create a reading via API
- Cards display correctly in UI
- Interpretation is coherent and Hermetic
- Response time < 10 seconds

---

## Phase 2: Users
**Target**: End of Week 4
**Goal**: Users can sign up, log in, and see reading history

### Deliverables
- [ ] Supabase Auth configured
- [ ] User profile page
- [ ] Protected routes
- [ ] Reading history list
- [ ] Reading detail view

### Success Criteria
- Can create account and log in
- Readings are saved to user's account
- Can view past readings
- Cannot access other users' readings

---

## Phase 3: Chat
**Target**: End of Week 5
**Goal**: Users can have follow-up conversations about readings

### Deliverables
- [ ] Conversation data model
- [ ] Chat API endpoint
- [ ] Streaming responses
- [ ] Chat UI in reading detail

### Success Criteria
- Can ask follow-up questions
- Responses stream in real-time
- Context from reading is maintained
- Conversation is saved

---

## Phase 4: Payments
**Target**: End of Week 6
**Goal**: Working subscription and credit purchase flow

### Deliverables
- [ ] Stripe products configured
- [ ] Checkout flow functional
- [ ] Webhook handler processing events
- [ ] Usage tracking for free tier
- [ ] Upgrade prompts

### Success Criteria
- Can subscribe to Seeker/Initiate
- Can purchase credits
- Subscription status updates correctly
- Free tier limits enforced

---

## Phase 5: Polish
**Target**: End of Week 7
**Goal**: Production-ready application

### Deliverables
- [ ] Landing page complete
- [ ] SEO optimized
- [ ] Error handling comprehensive
- [ ] Monitoring configured
- [ ] Legal pages published

### Success Criteria
- Lighthouse score > 90
- No unhandled errors
- Sentry capturing events
- Privacy/Terms accessible

---

## Launch
**Target**: Week 8
**Goal**: Live product with initial users

### Deliverables
- [ ] Production deployment complete
- [ ] DNS and SSL configured
- [ ] Payment processing live
- [ ] Analytics tracking
- [ ] Product Hunt submission

### Success Criteria
- Site accessible at production URL
- Can process real payments
- First 10 users signed up
- No critical bugs in first 24 hours

---

## Notes

### Weekly Review Questions
1. What was completed this week?
2. What blocked progress?
3. What's the priority for next week?
4. Any scope changes needed?

### Risk Register
| Risk | Mitigation |
|------|------------|
| LLM quality issues | Extensive prompt testing |
| Stripe integration complexity | Follow official guides |
| Time overrun | Ruthless scope prioritization |
| Card image licensing | Use public domain only |

