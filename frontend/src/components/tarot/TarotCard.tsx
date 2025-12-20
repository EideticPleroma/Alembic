import React from 'react';

import { cn } from '@/lib/utils';

interface TarotCardProps {
  card: {
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
  };
  position?: string;
  isReversed?: boolean;
  isRevealed?: boolean;
  onClick?: () => void;
}

const TarotCard = React.forwardRef<HTMLDivElement, TarotCardProps>(
  (
    {
      card,
      position,
      isReversed = false,
      isRevealed = true,
      onClick,
    },
    ref
  ) => {
    return (
      <div ref={ref} className="flex flex-col items-center w-full relative">
        {/* Card Image Container */}
        <div
          onClick={onClick}
          className={cn(
            'relative w-64 aspect-[2/3] cursor-pointer transition-all duration-500 transform origin-center',
            'hover:shadow-lg hover:scale-105',
            isReversed && 'rotate-180'
          )}
          style={{
            perspective: '1000px',
            transformStyle: 'preserve-3d',
          }}
        >
          {isRevealed ? (
            <div
              className={cn(
                'relative w-full h-full rounded-lg border-2 border-gold/50',
                'bg-gradient-to-br from-midnight/80 to-midnight/60',
                'overflow-hidden shadow-lg transition-all duration-300',
                'p-1'
              )}
            >
              {/* Radial gradient overlay */}
              <div
                className={cn(
                  'absolute inset-1 rounded-lg opacity-20 pointer-events-none z-10',
                  'bg-radial from-gold/30 to-transparent'
                )}
              />

              {/* Card image fills the entire container with padding */}
              <img
                src={card.image_url}
                alt={card.name}
                className="absolute inset-1 w-[calc(100%-0.5rem)] h-[calc(100%-0.5rem)] object-contain rounded opacity-90 hover:opacity-100 transition-opacity"
              />

              {/* Reversed Label - Positioned at bottom of card frame, appears on top when rotated */}
              {isReversed && (
                <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-gold text-xs font-bold text-center whitespace-nowrap z-20 -rotate-180">
                  Reversed
                </div>
              )}
            </div>
          ) : (
            <div className="w-full h-full rounded-lg border-2 border-gold/50 bg-gradient-to-br from-gold/20 to-gold/10 flex items-center justify-center shadow-lg">
              <div className="text-center">
                <div className="text-gold/60 text-2xl mb-2">?</div>
                <div className="text-xs text-gold/50 font-serif">Unrevealed</div>
              </div>
            </div>
          )}
        </div>

        {/* Text Below Card - Never Rotates - Only show when revealed */}
        {isRevealed && (
          <div className="relative z-10 text-center mt-4 w-full px-1">
            <h3 className="text-xs font-serif text-gold font-semibold leading-tight truncate w-full">
              {card.name}
            </h3>
            {position && (
              <p className="text-xs text-silver/70 font-light">{position}</p>
            )}
          </div>
        )}
      </div>
    );
  }
);

TarotCard.displayName = 'TarotCard';

export { TarotCard };
