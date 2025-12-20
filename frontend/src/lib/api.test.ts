import { describe, it, expect, vi, beforeEach } from 'vitest';
import { APIClient } from './api';
import type { Reading, Spread } from './types';

describe('APIClient', () => {
  let client: APIClient;

  beforeEach(() => {
    client = new APIClient('http://test-api');
    vi.resetAllMocks();
  });

  describe('GET requests', () => {
    it('makes GET requests with correct headers', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ data: 'test' }),
      });

      await client.get<{ data: string }>('/endpoint');

      expect(fetch).toHaveBeenCalledWith('http://test-api/endpoint', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
    });

    it('returns response data on success', async () => {
      const mockData = { id: '123', name: 'Test' };
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockData),
      });

      const result = await client.get<typeof mockData>('/endpoint');

      expect(result).toEqual(mockData);
    });

    it('throws error with detail message on non-ok response', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 404,
        json: () => Promise.resolve({ detail: 'Not found' }),
      });

      await expect(client.get('/missing')).rejects.toThrow('Not found');
    });

    it('throws generic error when detail is unavailable', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
        json: () => Promise.reject(new Error('Invalid JSON')),
      });

      await expect(client.get('/error')).rejects.toThrow(
        'API error: 500'
      );
    });
  });

  describe('POST requests', () => {
    it('sends data with correct method and headers', async () => {
      const postData = { question: 'What should I do?' };
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ id: '123' }),
      });

      await client.post('/reading', postData);

      expect(fetch).toHaveBeenCalledWith('http://test-api/reading', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(postData),
      });
    });

    it('handles POST request without data', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ success: true }),
      });

      await client.post('/action');

      expect(fetch).toHaveBeenCalledWith('http://test-api/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: undefined,
      });
    });

    it('returns response data from POST', async () => {
      const mockResponse = { id: '123', created: true };
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      const result = await client.post<typeof mockResponse>(
        '/reading',
        { question: 'Test' }
      );

      expect(result).toEqual(mockResponse);
    });
  });

  describe('PUT requests', () => {
    it('sends PUT request with data', async () => {
      const updateData = { status: 'updated' };
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ success: true }),
      });

      await client.put('/resource/123', updateData);

      expect(fetch).toHaveBeenCalledWith('http://test-api/resource/123', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updateData),
      });
    });
  });

  describe('DELETE requests', () => {
    it('sends DELETE request', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ deleted: true }),
      });

      await client.delete('/resource/123');

      expect(fetch).toHaveBeenCalledWith('http://test-api/resource/123', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
      });
    });
  });

  describe('Error handling', () => {
    it('constructs correct endpoint URL with method', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ data: 'test' }),
      });

      await client.get('/api/v1/readings');

      expect(fetch).toHaveBeenCalled();
      const calls = (global.fetch as ReturnType<typeof vi.fn>).mock.calls;
      const callArgs = calls[0];
      expect(callArgs[0]).toBe('http://test-api/api/v1/readings');
      expect((callArgs[1] as Record<string, unknown>).method).toBe('GET');
      expect((callArgs[1] as Record<string, unknown>).headers).toBeDefined();
    });

    it('constructs correct endpoint URL', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({}),
      });

      await client.get('/api/v1/readings');

      const calls = (global.fetch as ReturnType<typeof vi.fn>).mock.calls;
      const callArgs = calls[0];
      expect(callArgs[0]).toBe('http://test-api/api/v1/readings');
    });
  });

  describe('createReading', () => {
    it('sends correct payload to reading endpoint', async () => {
      const mockResponse: Reading = {
        id: 'reading-123',
        question: 'What should I do?',
        spread_type: 'three_card',
        cards: [],
        interpretation: 'Mock interpretation',
        created_at: new Date().toISOString(),
      };

      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      await client.createReading('What should I do?', 'three_card');

      expect(fetch).toHaveBeenCalledWith(
        'http://test-api/api/reading',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({
            question: 'What should I do?',
            spread_type: 'three_card',
          }),
        })
      );
    });

    it('returns reading data from API', async () => {
      const mockResponse: Reading = {
        id: 'reading-456',
        question: 'What is my path?',
        spread_type: 'three_card',
        cards: [
          {
            id: 'c1',
            name: 'Card 1',
            position: 'Past',
            is_reversed: false,
            image_url: '/c1.png',
          },
        ],
        interpretation: 'Test interpretation',
        created_at: '2025-12-19T00:00:00Z',
      };

      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      const result = await client.createReading('What is my path?', 'three_card');

      expect(result.id).toBe('reading-456');
      expect(result.question).toBe('What is my path?');
      expect(result.cards.length).toBe(1);
    });
  });

  describe('getSpreads', () => {
    it('calls correct endpoint', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve([]),
      });

      await client.getSpreads();

      expect(fetch).toHaveBeenCalledWith(
        'http://test-api/api/spreads',
        expect.objectContaining({
          method: 'GET',
        })
      );
    });

    it('returns array of spreads', async () => {
      const mockSpreads: Spread[] = [
        {
          name: 'Three Card',
          spread_id: 'three_card',
          description: 'A simple three-card spread',
          card_count: 3,
          positions: [
            {
              position: 0,
              name: 'Past',
              meaning: 'The past',
              guidance: 'What was?',
            },
          ],
          instructions: 'Draw three cards',
        },
        {
          name: 'Single Card',
          spread_id: 'one_card',
          description: 'A single card draw',
          card_count: 1,
          positions: [
            {
              position: 0,
              name: 'Message',
              meaning: 'The message',
              guidance: 'What now?',
            },
          ],
          instructions: 'Draw one card',
        },
      ];

      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockSpreads),
      });

      const result = await client.getSpreads();

      expect(result.length).toBe(2);
      expect(result[0].spread_id).toBe('three_card');
      expect(result[1].spread_id).toBe('one_card');
    });
  });
});
