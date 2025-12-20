'use client';

import { useEffect, useState } from 'react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { SpreadLayout, TarotCard } from '@/components/tarot';
import { apiClient } from '@/lib/api';
import { Reading, Spread, SpreadType } from '@/lib/types';

export default function ReadingPage() {
  const [spreads, setSpreads] = useState<Spread[]>([]);
  const [selectedSpread, setSelectedSpread] = useState<SpreadType>('three_card');
  const [question, setQuestion] = useState('');
  const [reading, setReading] = useState<Reading | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loadingSpreads, setLoadingSpreads] = useState(true);

  useEffect(() => {
    const loadSpreads = async () => {
      try {
        const data = await apiClient.getSpreads();
        setSpreads(data);
        setLoadingSpreads(false);
      } catch (err) {
        setError('Failed to load spreads');
        setLoadingSpreads(false);
      }
    };

    loadSpreads();
  }, []);

  const handleCreateReading = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!question.trim()) {
      setError('Please enter a question');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await apiClient.createReading(question, selectedSpread);
      setReading(result);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Failed to create reading'
      );
    } finally {
      setLoading(false);
    }
  };

  const currentSpread = spreads.find((s) => s.spread_id === selectedSpread);

  return (
    <main className="min-h-screen bg-gradient-void p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="font-serif text-4xl font-bold text-gold mb-2">
          Alembic Reading
        </h1>
        <p className="text-silver/70 mb-8">
          Seek guidance through the archetypal wisdom of the cards
        </p>

        {!reading ? (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-1">
              <div className="bg-midnight/50 rounded-lg p-6 border border-gold/30 sticky top-8">
                <h2 className="font-serif text-2xl text-gold mb-6">
                  New Reading
                </h2>

                <form onSubmit={handleCreateReading} className="space-y-4">
                  <div>
                    <label className="block text-sm font-semibold text-gold mb-2">
                      Spread Type
                    </label>
                    {loadingSpreads ? (
                      <div className="text-silver/50">Loading spreads...</div>
                    ) : (
                      <select
                        value={selectedSpread}
                        onChange={(e) => setSelectedSpread(e.target.value as SpreadType)}
                        className="w-full px-4 py-2 bg-midnight border border-gold/30 text-cream rounded focus:outline-none focus:ring-2 focus:ring-gold/50"
                      >
                        {spreads.map((spread) => (
                          <option key={spread.spread_id} value={spread.spread_id}>
                            {spread.name}
                          </option>
                        ))}
                      </select>
                    )}
                    {currentSpread && (
                      <p className="text-xs text-silver/60 mt-2">
                        {currentSpread.description}
                      </p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gold mb-2">
                      Your Question
                    </label>
                    <Textarea
                      value={question}
                      onChange={(e) => setQuestion(e.target.value)}
                      placeholder="What would you like guidance on?"
                      className="w-full px-4 py-2 bg-midnight border border-gold/30 text-cream rounded focus:outline-none focus:ring-2 focus:ring-gold/50 placeholder-silver/30 min-h-24"
                      disabled={loading}
                    />
                    <p className="text-xs text-silver/50 mt-1">
                      {question.length} / 1000 characters
                    </p>
                  </div>

                  {error && (
                    <div className="p-3 bg-red-900/30 border border-red-500/50 rounded text-red-200 text-sm">
                      {error}
                    </div>
                  )}

                  <Button
                    type="submit"
                    disabled={loading || !question.trim()}
                    className="w-full bg-gold text-midnight hover:bg-gold/80 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? 'Drawing Cards...' : 'Get Reading'}
                  </Button>
                </form>
              </div>
            </div>

            <div className="lg:col-span-2">
              <div className="bg-midnight/50 rounded-lg p-8 border border-gold/30 h-full flex items-center justify-center min-h-96">
                <p className="text-cream/60 text-center">
                  {loadingSpreads
                    ? 'Loading spreads...'
                    : 'Enter a question and select a spread to begin your reading'}
                </p>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-8">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2">
                <div className="bg-midnight/50 rounded-lg p-8 border border-gold/30">
                  <h2 className="font-serif text-2xl text-gold mb-6">
                    {currentSpread?.name} Reading
                  </h2>

                  <div className="mb-8">
                    <p className="text-silver/70 mb-4">
                      <span className="text-gold font-semibold">Your Question:</span> {reading.question}
                    </p>
                  </div>

                  <div className="mb-8">
                    <SpreadLayout
                      spreadType={selectedSpread}
                      cards={reading.cards}
                    />
                  </div>
                </div>
              </div>

              <div className="lg:col-span-1">
                <div className="bg-midnight/50 rounded-lg p-6 border border-gold/30 sticky top-8">
                  <h3 className="font-serif text-xl text-gold mb-4">
                    Interpretation
                  </h3>
                  <p className="text-cream/80 leading-relaxed text-sm">
                    {reading.interpretation}
                  </p>
                </div>
              </div>
            </div>

            <div className="flex justify-center">
              <Button
                onClick={() => {
                  setReading(null);
                  setQuestion('');
                  setError(null);
                }}
                className="bg-gold text-midnight hover:bg-gold/80"
              >
                New Reading
              </Button>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
