'use client';

import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

interface CardData {
  id: string;
  name: string;
  image_url: string;
  number?: number;
  numeral?: string;
  keywords?: string[];
  archetype?: string;
  hermetic_principle?: string;
  upright?: string;
  reversed?: string;
}

interface CardDetailModalProps {
  card: CardData | null;
  isReversed: boolean;
  isOpen: boolean;
  onClose: () => void;
}

const CardDetailModal: React.FC<CardDetailModalProps> = ({
  card,
  isReversed,
  isOpen,
  onClose,
}) => {
  if (!isOpen || !card) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div
          className={cn(
            'bg-midnight/95 border-2 border-gold/50 rounded-lg',
            'max-w-2xl w-full max-h-[90vh] overflow-y-auto',
            'shadow-2xl'
          )}
          onClick={(e) => e.stopPropagation()}
        >
          {/* Close Button */}
          <div className="sticky top-0 flex justify-end p-4 bg-midnight/80 border-b border-gold/20">
            <button
              onClick={onClose}
              className="text-gold/70 hover:text-gold transition-colors"
              aria-label="Close"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>

          {/* Content */}
          <div className="p-8 space-y-6">
            {/* Header with Card Image */}
            <div className="flex gap-6">
              {/* Card Image */}
              <div className="flex-shrink-0">
                <div
                  className={cn(
                    'relative w-40 aspect-[2/3] rounded-lg border-2 border-gold/50',
                    'bg-gradient-to-br from-midnight/80 to-midnight/60',
                    'overflow-hidden shadow-lg',
                    'flex items-center justify-center p-1',
                    isReversed && 'rotate-180'
                  )}
                >
                  <div className="absolute inset-1 rounded-lg opacity-20 pointer-events-none z-10 bg-radial from-gold/30 to-transparent" />
                  <img
                    src={card.image_url}
                    alt={card.name}
                    className="relative z-0 w-full h-full object-contain rounded opacity-90"
                  />
                </div>
              </div>

              {/* Card Info */}
              <div className="flex-1 space-y-3">
                <div>
                  <h2 className="font-serif text-3xl text-gold font-bold">
                    {card.name}
                  </h2>
                  {card.numeral && (
                    <p className="text-lg text-gold/70 font-serif">
                      {card.numeral}
                    </p>
                  )}
                </div>

                {isReversed && (
                  <div className="inline-block px-3 py-1 bg-gold/20 border border-gold/50 rounded">
                    <p className="text-sm text-gold font-semibold">Reversed</p>
                  </div>
                )}

                {card.archetype && (
                  <div>
                    <p className="text-xs text-silver/60 uppercase tracking-wide">
                      Archetype
                    </p>
                    <p className="text-cream/90">{card.archetype}</p>
                  </div>
                )}

                {card.hermetic_principle && (
                  <div>
                    <p className="text-xs text-silver/60 uppercase tracking-wide">
                      Hermetic Principle
                    </p>
                    <p className="text-cream/90">{card.hermetic_principle}</p>
                  </div>
                )}

                {card.keywords && card.keywords.length > 0 && (
                  <div>
                    <p className="text-xs text-silver/60 uppercase tracking-wide mb-2">
                      Keywords
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {card.keywords.map((keyword) => (
                        <span
                          key={keyword}
                          className="px-2 py-1 bg-gold/10 border border-gold/30 rounded text-xs text-cream/80"
                        >
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Meanings */}
            <div className="border-t border-gold/20 pt-6 space-y-6">
              {/* Upright */}
              <div>
                <h3 className="font-serif text-xl text-gold mb-3 flex items-center gap-2">
                  <span className="text-lg">+</span> Upright Meaning
                </h3>
                <p className="text-cream/80 leading-relaxed">
                  {card.upright}
                </p>
              </div>

              {/* Reversed */}
              {card.reversed && (
                <div>
                  <h3 className="font-serif text-xl text-gold mb-3 flex items-center gap-2">
                    <span className="text-lg">↻</span> Reversed Meaning
                  </h3>
                  <p className="text-cream/80 leading-relaxed">
                    {card.reversed}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Footer */}
          <div className="sticky bottom-0 flex justify-end p-4 bg-midnight/80 border-t border-gold/20">
            <Button
              onClick={onClose}
              className="bg-gold text-midnight hover:bg-gold/80"
            >
              Close
            </Button>
          </div>
        </div>
      </div>
    </>
  );
};

export { CardDetailModal };
