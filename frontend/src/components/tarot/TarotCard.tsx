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
      <div
        ref={ref}
        onClick={onClick}
        className={cn(
          'relative h-48 w-32 cursor-pointer transition-all duration-500 transform',
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
              'flex flex-col items-center justify-between p-3',
              isReversed && 'rotate-180'
            )}
          >
            <div
              className={cn(
                'absolute inset-0 rounded-lg opacity-20 pointer-events-none',
                'bg-radial from-gold/30 to-transparent'
              )}
            />

            <div className="relative z-10 text-center">
              <img
                src={card.image_url}
                alt={card.name}
                className="w-24 h-32 object-cover rounded opacity-80 hover:opacity-100 transition-opacity"
              />
            </div>

            <div className="relative z-10 text-center">
              <h3 className="text-xs font-serif text-gold font-semibold leading-tight truncate w-full">
                {card.name}
              </h3>
              {position && (
                <p className="text-xs text-silver/70 mt-1 font-light">{position}</p>
              )}
            </div>

            {isReversed && (
              <div className="absolute top-1 right-1 z-20 text-gold text-xs font-bold">
                Rev.
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
    );
  }
);

TarotCard.displayName = 'TarotCard';

export { TarotCard };
