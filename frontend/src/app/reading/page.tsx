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
 * Handles both ## headers and ### headers, with fallbacks for unstructured content.
 */
function InterpretationContent({ content }: { content: string }) {
  // Helper to render card sections (### headers)
  const renderCardSections = (text: string) => {
    const cardSections = text.split(/### /).filter(Boolean);
    
    return (
      <div className="space-y-4">
        {cardSections.map((cardSection, idx) => {
          const cardLines = cardSection.split('\n');
          const cardTitle = cardLines[0].trim();
          const cardBody = cardLines.slice(1).join('\n').trim();

          if (!cardBody) return null;

          return (
            <div key={idx} className="bg-midnight/30 rounded-lg p-4 border border-gold/10">
              <h5 className="font-semibold text-gold/90 text-sm mb-2">
                {cardTitle}
              </h5>
              <p className="text-cream/80 leading-relaxed text-sm">
                {cardBody}
              </p>
            </div>
          );
        })}
      </div>
    );
  };

  // Helper to render reflection questions
  const renderReflectionQuestions = (text: string) => {
    let bullets: string[] = [];
    
    // Check for bullet points
    if (text.includes('\n- ') || text.startsWith('- ')) {
      bullets = text
        .split(/\n- /)
        .filter(Boolean)
        .map((b) => b.replace(/^- /, '').trim());
    }
    // Check for numbered list (1. 2. 3. etc)
    else if (/\d+\.\s/.test(text)) {
      bullets = text
        .split(/\n?\d+\.\s+/)
        .filter(Boolean)
        .map((b) => b.trim());
    }
    // Fallback: split by question marks or newlines
    else {
      bullets = text
        .split(/\?\s*/)
        .filter((line) => line.trim().length > 0)
        .map((b) => b.trim() + '?');
    }

    return (
      <ul className="space-y-2">
        {bullets.map((bullet, idx) => (
          <li
            key={idx}
            className="text-cream/80 text-sm pl-4 relative before:content-[''] before:absolute before:left-0 before:top-2 before:w-1.5 before:h-1.5 before:bg-gold/60 before:rounded-full"
          >
            {bullet}
          </li>
        ))}
      </ul>
    );
  };

  // Check if content has ## headers
  const hasMainHeaders = content.includes('## ');
  // Check if content has ### headers (card sections)
  const hasCardHeaders = content.includes('### ');

  // If we have ## headers, split by them
  if (hasMainHeaders) {
    const sections = content.split(/^## /gm).filter(Boolean);

    return (
      <div className="space-y-6">
        {sections.map((rawSection, index) => {
          const lines = rawSection.split('\n');
          const headerTitle = lines[0].trim();
          const bodyLines = lines.slice(1).join('\n').trim();

          if (!bodyLines) return null;

          // Handle Reflection Questions
          if (headerTitle.toLowerCase().includes('reflection question')) {
            return (
              <div key={index} className="mb-6">
                <h4 className="font-serif text-lg text-gold mb-3 border-b border-gold/20 pb-1">
                  {headerTitle}
                </h4>
                {renderReflectionQuestions(bodyLines)}
              </div>
            );
          }

          // Handle Cards Speak section
          if (headerTitle.toLowerCase().includes('cards speak') || bodyLines.includes('### ')) {
            return (
              <div key={index} className="mb-6">
                <h4 className="font-serif text-lg text-gold mb-4 border-b border-gold/20 pb-1">
                  {headerTitle}
                </h4>
                {renderCardSections(bodyLines)}
              </div>
            );
          }

          // Handle The Weaving section
          if (headerTitle.toLowerCase().includes('weaving')) {
            return (
              <div key={index} className="mb-6">
                <h4 className="font-serif text-lg text-gold mb-3 border-b border-gold/20 pb-1">
                  {headerTitle}
                </h4>
                <div className="bg-gold/5 rounded-lg p-4 border-l-2 border-gold/50">
                  <p className="text-cream/80 leading-relaxed text-sm italic">
                    {bodyLines}
                  </p>
                </div>
              </div>
            );
          }

          // Default section
          return (
            <div key={index} className="mb-6">
              <h4 className="font-serif text-lg text-gold mb-3 border-b border-gold/20 pb-1">
                {headerTitle}
              </h4>
              <p className="text-cream/80 leading-relaxed text-sm">{bodyLines}</p>
            </div>
          );
        }).filter(Boolean)}
      </div>
    );
  }

  // If no ## headers but has ### headers, parse by those
  if (hasCardHeaders) {
    // Try to extract sections by known keywords
    const parts: { title: string; content: string }[] = [];
    
    // Extract card sections (everything before "The Weaving" or "Reflection")
    const weavingMatch = content.match(/The Weaving\s*([\s\S]*?)(?=Reflection Questions|$)/i);
    const reflectionMatch = content.match(/Reflection Questions?\s*([\s\S]*?)$/i);
    
    // Get card content (everything with ### headers before weaving/reflection)
    let cardContent = content;
    if (weavingMatch) {
      cardContent = content.substring(0, content.indexOf(weavingMatch[0]));
    } else if (reflectionMatch) {
      cardContent = content.substring(0, content.indexOf(reflectionMatch[0]));
    }

    return (
      <div className="space-y-6">
        {/* Card Sections */}
        {cardContent.includes('### ') && (
          <div className="mb-6">
            <h4 className="font-serif text-lg text-gold mb-4 border-b border-gold/20 pb-1">
              The Cards Speak
            </h4>
            {renderCardSections(cardContent)}
          </div>
        )}

        {/* The Weaving */}
        {weavingMatch && (
          <div className="mb-6">
            <h4 className="font-serif text-lg text-gold mb-3 border-b border-gold/20 pb-1">
              The Weaving
            </h4>
            <div className="bg-gold/5 rounded-lg p-4 border-l-2 border-gold/50">
              <p className="text-cream/80 leading-relaxed text-sm italic">
                {weavingMatch[1].trim()}
              </p>
            </div>
          </div>
        )}

        {/* Reflection Questions */}
        {reflectionMatch && (
          <div className="mb-6">
            <h4 className="font-serif text-lg text-gold mb-3 border-b border-gold/20 pb-1">
              Reflection Questions
            </h4>
            {renderReflectionQuestions(reflectionMatch[1].trim())}
          </div>
        )}
      </div>
    );
  }

  // Fallback: render as plain text with paragraphs
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
