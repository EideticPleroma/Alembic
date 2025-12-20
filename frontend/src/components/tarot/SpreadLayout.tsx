import React from 'react';

import { cn } from '@/lib/utils';
import { TarotCard } from './TarotCard';

interface Card {
  id: string;
  name: string;
  position: string;
  is_reversed: boolean;
  image_url: string;
}

interface SpreadLayoutProps {
  spreadType: 'one_card' | 'three_card' | 'shadow_work' | 'celtic_cross';
  cards: Card[];
  onCardClick?: (cardIndex: number) => void;
}

const SpreadLayout = React.forwardRef<HTMLDivElement, SpreadLayoutProps>(
  ({ spreadType, cards, onCardClick }, ref) => {
    const getLayoutClasses = () => {
      switch (spreadType) {
        case 'one_card':
          return 'flex justify-center items-center';
        case 'three_card':
          return 'flex justify-center items-center gap-12';
        case 'shadow_work':
          return 'flex justify-center items-center gap-8';
        case 'celtic_cross':
          return 'grid grid-cols-3 gap-4 justify-center items-center w-fit mx-auto';
        default:
          return 'flex justify-center items-center gap-8';
      }
    };

    const getCardGridPosition = (index: number) => {
      if (spreadType !== 'celtic_cross') return '';

      const positions: Record<number, string> = {
        0: 'col-start-2',
        1: 'col-start-1 row-start-2',
        2: 'col-start-2 row-start-2',
        3: 'col-start-3 row-start-2',
        4: 'col-start-2 row-start-3',
        5: 'col-start-1 row-start-4',
        6: 'col-start-2 row-start-4',
        7: 'col-start-3 row-start-4',
        8: 'col-start-2 row-start-5',
        9: 'col-start-2 row-start-6',
      };

      return positions[index] || '';
    };

    const renderCards = () => {
      return cards.map((card, index) => (
        <div
          key={`${card.id}-${index}`}
          className={cn('flex justify-center items-center', getCardGridPosition(index))}
          onClick={() => onCardClick?.(index)}
        >
          <TarotCard
            card={card}
            position={card.position}
            isReversed={card.is_reversed}
            isRevealed={true}
          />
        </div>
      ));
    };

    return (
      <div
        ref={ref}
        className={cn(
          'w-full py-8 px-4',
          'flex justify-center items-center'
        )}
      >
        <div className={getLayoutClasses()}>
          {renderCards()}
        </div>
      </div>
    );
  }
);

SpreadLayout.displayName = 'SpreadLayout';

export { SpreadLayout };
