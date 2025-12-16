# End-to-End Tests

E2E tests verify complete user journeys in a real browser environment.

## Future Setup

We'll use **Playwright** for E2E testing:

```bash
npm install -D @playwright/test
npx playwright install
```

## Structure

```
src/__tests__/e2e/
  reading.spec.ts          # Complete reading flow
  auth.spec.ts             # Authentication flow
  payment.spec.ts          # Subscription flow
  fixtures/
    auth.setup.ts          # Login fixture
```

## Example (Playwright)

```typescript
import { test, expect } from '@playwright/test';

test('user completes a reading', async ({ page }) => {
  await page.goto('http://localhost:3000');
  
  // Click begin reading button
  await page.click('button:has-text("Begin Reading")');
  
  // Enter question
  await page.fill('input[placeholder*="question"]', 'What should I focus on?');
  
  // Submit
  await page.click('button:has-text("Draw Cards")');
  
  // Verify cards appear
  await expect(page.locator('text=The Fool')).toBeVisible();
  await expect(page.locator('text=/interpretation/i')).toBeVisible();
});
```

## When to Add E2E Tests

1. After completing a major user flow
2. For critical paths (signup → reading → payment)
3. Before major releases to verify no regressions
4. For cross-browser compatibility testing

## Running Tests

```bash
npm run test:e2e
npm run test:e2e -- --debug
npm run test:e2e -- --ui
```

## CI/CD Integration

E2E tests run in CI pipeline on every PR:
- Test against staging environment
- Capture videos on failure
- Generate reports
