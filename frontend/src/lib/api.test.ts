import { describe, it, expect, vi, beforeEach } from 'vitest';
import { APIClient } from './api';

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
});
