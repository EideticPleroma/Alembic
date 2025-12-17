# Integration Tests

Integration tests verify interactions between multiple components and systems.

## Structure

- Test multiple components working together
- Use mocked API responses (MSW)
- Test data flow between components
- Verify error handling across component boundaries

## Example

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@/test/utils';
import { server } from '@/test/mocks/server';

describe('Reading Flow Integration', () => {
  beforeAll(() => server.listen());
  afterAll(() => server.close());

  it('completes full reading submission', async () => {
    render(<ReadingPage />);

    // User enters question
    const input = screen.getByPlaceholderText(/enter your question/i);
    fireEvent.change(input, { target: { value: 'What lies ahead?' } });

    // User submits
    fireEvent.click(screen.getByRole('button', { name: /draw cards/i }));

    // Cards appear
    await waitFor(() => {
      expect(screen.getByText(/the fool/i)).toBeInTheDocument();
    });
  });
});
```

## When to Add Integration Tests

1. After completing a feature with multiple components
2. When fixing bugs that involve component interactions
3. For critical user flows (reading creation, payment flow)
4. When testing error states across multiple layers

## Running Tests

```bash
npm test -- __tests__/integration
```
