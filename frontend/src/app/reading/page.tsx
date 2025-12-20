'use client';

import { useEffect, useState } from 'react';

import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { SpreadLayout, CardDetailModal } from '@/components/tarot';
import { apiClient } from '@/lib/api';
import { Reading, Spread, SpreadType, CardInReading } from '@/lib/types';

/**
 * Renders structured interpretation content with proper formatting.
 * Parses markdown-like structure from LLM response.
 */
function InterpretationContent({ content }: { content: string }) {
  // Parse the content into sections
  const sections = content.split(/(?=^## )/gm).filter(Boolean);

  const renderSection = (section: string, index: number) => {
    const lines = section.trim().split('\n');
    const headerMatch = lines[0].match(/^##\s+(.+)/);

    if (!headerMatch) {
      // Plain paragraph
      return (
        <p key={index} className="text-cream/80 leading-relaxed mb-4">
          {section}
        </p>
      );
    }

    const headerTitle = headerMatch[1];
    const bodyLines = lines.slice(1).join('\n').trim();

    // Check for subsections (### headers)
    const hasSubsections = bodyLines.includes('### ');

    if (hasSubsections) {
      const subsections = bodyLines.split(/(?=^### )/gm).filter(Boolean);

      return (
        <div key={index} className="mb-6">
          <h4 className="font-serif text-lg text-gold mb-3 border-b border-gold/20 pb-1">
            {headerTitle}
          </h4>
          {subsections.map((sub, subIndex) => {
            const subLines = sub.trim().split('\n');
            const subHeaderMatch = subLines[0].match(/^###\s+(.+)/);

            if (!subHeaderMatch) {
              return (
                <p key={subIndex} className="text-cream/80 leading-relaxed mb-3">
                  {sub}
                </p>
              );
            }

            const subTitle = subHeaderMatch[1];
            const subBody = subLines.slice(1).join('\n').trim();

            return (
              <div key={subIndex} className="mb-4">
                <h5 className="font-semibold text-gold/90 text-sm mb-1">
                  {subTitle}
                </h5>
                <p className="text-cream/80 leading-relaxed text-sm pl-2 border-l-2 border-gold/20">
                  {subBody}
                </p>
              </div>
            );
          })}
        </div>
      );
    }

    // Check for bullet points
    const hasBullets = bodyLines.includes('\n- ');

    if (hasBullets) {
      const bulletParts = bodyLines.split(/(?=^- )/gm);
      const intro = bulletParts[0].trim();
      const bullets = bulletParts.slice(1).map((b) => b.replace(/^- /, '').trim());

      return (
        <div key={index} className="mb-6">
          <h4 className="font-serif text-lg text-gold mb-3 border-b border-gold/20 pb-1">
            {headerTitle}
          </h4>
          {intro && (
            <p className="text-cream/80 leading-relaxed mb-3 text-sm">{intro}</p>
          )}
          <ul className="space-y-2">
            {bullets.map((bullet, bulletIndex) => (
              <li
                key={bulletIndex}
                className="text-cream/80 text-sm pl-4 relative before:content-[''] before:absolute before:left-0 before:top-2 before:w-1.5 before:h-1.5 before:bg-gold/60 before:rounded-full"
              >
                {bullet}
              </li>
            ))}
          </ul>
        </div>
      );
    }

    // Regular section with body
    return (
      <div key={index} className="mb-6">
        <h4 className="font-serif text-lg text-gold mb-3 border-b border-gold/20 pb-1">
          {headerTitle}
        </h4>
        <p className="text-cream/80 leading-relaxed text-sm">{bodyLines}</p>
      </div>
    );
  };

  // If no structured content detected, render as plain text with paragraphs
  if (!content.includes('## ')) {
    return (
      <div className="space-y-4">
        {content.split('\n\n').map((paragraph, index) => (
          <p key={index} className="text-cream/80 leading-relaxed text-sm">
            {paragraph}
          </p>
        ))}
      </div>
    );
  }

  return <div>{sections.map(renderSection)}</div>;
}

export default function ReadingPage() {
  const [spreads, setSpreads] = useState<Spread[]>([]);
  const [selectedSpread, setSelectedSpread] = useState<SpreadType>('three_card');
  const [question, setQuestion] = useState('');
  const [reading, setReading] = useState<Reading | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loadingSpreads, setLoadingSpreads] = useState(true);
  const [selectedCard, setSelectedCard] = useState<CardInReading | null>(null);
  const [selectedCardReversed, setSelectedCardReversed] = useState(false);
  const [isCardModalOpen, setIsCardModalOpen] = useState(false);

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

  const handleCardClick = (cardIndex: number) => {
    if (reading && reading.cards[cardIndex]) {
      const card = reading.cards[cardIndex];
      setSelectedCard(card);
      setSelectedCardReversed(card.is_reversed);
      setIsCardModalOpen(true);
    }
  };

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
            {/* Cards Section - Full Width */}
            <div className="bg-midnight/50 rounded-lg p-8 border border-gold/30">
              <h2 className="font-serif text-2xl text-gold mb-2">
                {currentSpread?.name} Reading
              </h2>
              <p className="text-silver/70 mb-6">
                <span className="text-gold font-semibold">Your Question:</span> {reading.question}
              </p>

              <div className="flex justify-center">
                <SpreadLayout
                  spreadType={selectedSpread}
                  cards={reading.cards}
                  onCardClick={handleCardClick}
                />
              </div>
            </div>

            {/* Interpretation Section - Full Width, Stacked */}
            <div className="space-y-6">
              {/* Interpretation */}
              <div className="bg-midnight/50 rounded-lg p-8 border border-gold/30">
                <h3 className="font-serif text-2xl text-gold mb-6">
                  Interpretation
                </h3>
                <div className="prose prose-sm prose-invert max-w-none">
                  <InterpretationContent content={reading.interpretation} />
                </div>
              </div>
            </div>

            {/* New Reading Button */}
            <div className="flex justify-center pt-4">
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

      <CardDetailModal
        card={selectedCard}
        isReversed={selectedCardReversed}
        isOpen={isCardModalOpen}
        onClose={() => setIsCardModalOpen(false)}
      />
    </main>
  );
}
