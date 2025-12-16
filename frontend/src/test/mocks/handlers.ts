import { http, HttpResponse } from 'msw';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const handlers = [
  // Example API handlers - add more as needed
  http.get(`${API_URL}/health`, () => {
    return HttpResponse.json({ status: 'ok' });
  }),

  http.post(`${API_URL}/reading`, () => {
    return HttpResponse.json({
      id: 'test-reading-123',
      cards: [
        { id: 'card_0', name: 'The Fool', position: 'Past' },
        { id: 'card_1', name: 'The Magician', position: 'Present' },
        { id: 'card_2', name: 'The Priestess', position: 'Future' },
      ],
      interpretation: 'A test reading interpretation.',
      created_at: new Date().toISOString(),
    });
  }),
];
