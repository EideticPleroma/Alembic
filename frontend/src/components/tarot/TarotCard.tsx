import React from 'react';

import { cn } from '@/lib/utils';

interface TarotCardProps {
  card: {
    id: string;
    name: string;
    image_url: string;
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
      <div ref={ref} className="flex flex-col items-center w-full">
        {/* Card Image Container */}
        <div
          onClick={onClick}
          className={cn(
            'relative w-full aspect-video cursor-pointer transition-all duration-500 transform',
            'hover:shadow-lg hover:scale-105',
            isReversed && !isRevealed && '[transform:rotateY(180deg)]'
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
                'flex flex-col items-center justify-center p-2',
                isReversed && 'rotate-180'
              )}
            >
              <div
                className={cn(
                  'absolute inset-0 rounded-lg opacity-20 pointer-events-none',
                  'bg-radial from-gold/30 to-transparent'
                )}
              />

              {isReversed && (
                <div className="absolute top-2 left-2 right-2 z-20 text-gold text-xs font-bold text-center">
                  Rev.
                </div>
              )}

              <div className="relative z-10 flex-1 flex items-center justify-center min-w-0 w-full">
                <img
                  src={card.image_url}
                  alt={card.name}
                  className="w-full h-full object-contain rounded opacity-90 hover:opacity-100 transition-opacity"
                />
              </div>
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
          <div className="relative z-10 text-center mt-2 w-full px-1">
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
