# Testing and Code Quality Guide

This document outlines the testing setup and code quality practices for the Alembic frontend.

## Quick Start

### Running Tests

```bash
# Run all tests once
npm test -- --run

# Run tests in watch mode
npm test

# Run tests with UI
npm run test:ui

# Generate coverage report
npm run test:coverage
```

### Code Quality

```bash
# Type checking
npm run type-check

# Linting
npm run lint

# Format code
npm run format

# Check formatting without changes
npm run format:check
```

## Test Structure

### Unit Tests

Located alongside source files with `.test.ts` or `.test.tsx` extension.

**Current coverage:**
- `src/lib/utils.ts` - 100% (9 tests)
- `src/lib/api.ts` - 100% (11 tests)
- `src/components/ui/button.tsx` - 100% (11 tests)
- `src/components/ui/card.tsx` - 100% (10 tests)
- `src/components/ui/input.tsx` - 100% (10 tests)

### Integration Tests

Located in `src/__tests__/integration/`

**Purpose**: Test multiple components working together, component interactions, and data flow.

**Getting started**:
```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@/test/utils';
import { server } from '@/test/mocks/server';

describe('Feature Integration', () => {
  beforeAll(() => server.listen());
  afterAll(() => server.close());

  it('completes user flow', async () => {
    // Test implementation
  });
});
```

### E2E Tests

Located in `src/__tests__/e2e/`

**Purpose**: Test complete user journeys in a real browser environment.

**Setup**: Uses Playwright (to be installed)

```bash
npm install -D @playwright/test
npx playwright install
```

## Mocking Strategy

### API Mocking

We use Mock Service Worker (MSW) for API mocking:

```typescript
import { server } from '@/test/mocks/server';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

Add new handlers in `src/test/mocks/handlers.ts`:

```typescript
http.post(`${API_URL}/reading`, () => {
  return HttpResponse.json({
    id: 'test-123',
    cards: [...],
  });
}),
```

### Component Testing

Use the custom `render` function from `@/test/utils`:

```typescript
import { render, screen } from '@/test/utils';
```

This wraps components with necessary providers.

## Pre-commit Hooks

Husky + lint-staged automatically run before commit:

1. **Pre-commit**: Linting, formatting, type checking on staged files
2. **Pre-push**: Full test suite must pass

These are configured in:
- `.husky/pre-commit`
- `.husky/pre-push`
- `.lintstagedrc.json`

## Code Coverage

Current coverage:
- **Statements**: 60.21%
- **Branches**: 80%
- **Functions**: 61.53%
- **Lines**: 60.21%

**Target coverage**:
- Core utilities: 100%
- Components: 90%
- Services: 85%

Generate report:
```bash
npm run test:coverage
```

Report available at `coverage/lcov-report/index.html`

## Best Practices

### What to Test

- Business logic and calculations
- Error handling and edge cases
- Component rendering and interactions
- API client methods
- Utility functions

### What NOT to Test

- Third-party libraries
- Framework internals
- Trivial getters/setters
- Implementation details that might change

### Testing Tips

1. **Test behavior, not implementation**
   - ✓ "Button is disabled when isLoading is true"
   - ✗ "Component sets this.state.disabled to true"

2. **Use descriptive test names**
   - ✓ "displays error message when API returns 400"
   - ✗ "handles error"

3. **Keep tests focused**
   - One assertion per test when possible
   - Use `beforeEach` for setup

4. **Mock external dependencies**
   - API calls
   - Timers
   - Local storage

## Debugging Tests

### Run single test file

```bash
npm test -- src/lib/utils.test.ts
```

### Debug in browser

```bash
npm run test:ui
```

Opens interactive test UI at `http://localhost:51204/`

### Watch mode with pattern

```bash
npm test -- --watch --grep "Button"
```

## Continuous Integration

Tests run automatically on:
- Every commit (pre-commit hook)
- Before push (pre-push hook)
- Pull requests (GitHub Actions - when configured)

## Resources

- [Vitest Documentation](https://vitest.dev/)
- [Testing Library](https://testing-library.com/react)
- [Mock Service Worker](https://mswjs.io/)
- [Playwright](https://playwright.dev/)

## Next Steps

1. Add integration tests for reading flow
2. Set up E2E tests with Playwright
3. Configure GitHub Actions CI/CD
4. Increase test coverage to 80%+
