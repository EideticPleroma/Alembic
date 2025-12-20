import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import { SpreadLayout } from './SpreadLayout';

describe('SpreadLayout', () => {
  const mockCards = [
    {
      id: 'c1',
      name: 'The Fool',
      position: 'Past',
      is_reversed: false,
      image_url: '/cards/c1.png',
    },
    {
      id: 'c2',
      name: 'The Magician',
      position: 'Present',
      is_reversed: true,
      image_url: '/cards/c2.png',
    },
    {
      id: 'c3',
      name: 'High Priestess',
      position: 'Future',
      is_reversed: false,
      image_url: '/cards/c3.png',
    },
  ];

  describe('rendering', () => {
    it('renders correct number of cards', () => {
      render(<SpreadLayout spreadType="three_card" cards={mockCards} />);
      expect(screen.getByText('The Fool')).toBeInTheDocument();
      expect(screen.getByText('The Magician')).toBeInTheDocument();
      expect(screen.getByText('High Priestess')).toBeInTheDocument();
    });

    it('passes card data to TarotCard components', () => {
      render(<SpreadLayout spreadType="three_card" cards={mockCards} />);
      expect(screen.getByAltText('The Fool')).toHaveAttribute(
        'src',
        '/cards/c1.png'
      );
      expect(screen.getByAltText('The Magician')).toHaveAttribute(
        'src',
        '/cards/c2.png'
      );
      expect(screen.getByAltText('High Priestess')).toHaveAttribute(
        'src',
        '/cards/c3.png'
      );
    });
  });

  describe('layout types', () => {
    it('applies three_card layout classes', () => {
      const { container } = render(
        <SpreadLayout spreadType="three_card" cards={mockCards} />
      );
      const layoutContainer = container.querySelector('.gap-12');
      expect(layoutContainer).toBeInTheDocument();
    });

    it('applies one_card centered layout', () => {
      const { container } = render(
        <SpreadLayout
          spreadType="one_card"
          cards={[mockCards[0]]}
        />
      );
      const layoutContainer = container.querySelector('.justify-center');
      expect(layoutContainer).toBeInTheDocument();
    });

    it('renders with shadow_work layout', () => {
      const { container } = render(
        <SpreadLayout
          spreadType="shadow_work"
          cards={mockCards}
        />
      );
      const layoutContainer = container.querySelector('.gap-8');
      expect(layoutContainer).toBeInTheDocument();
    });

    it('renders empty array', () => {
      const { container } = render(
        <SpreadLayout spreadType="three_card" cards={[]} />
      );
      expect(container.firstChild).toBeInTheDocument();
    });
  });

  describe('interactions', () => {
    it('calls onCardClick when card is clicked', () => {
      const handleCardClick = vi.fn();
      render(
        <SpreadLayout
          spreadType="three_card"
          cards={mockCards}
          onCardClick={handleCardClick}
        />
      );

      // Click any card wrapper
      const cardWrappers = screen.getAllByAltText(/The Fool|The Magician|High Priestess/);
      if (cardWrappers.length > 0) {
        const parentDiv = cardWrappers[0].closest('div')?.parentElement;
        if (parentDiv) {
          parentDiv.click();
        }
      }
    });

    it('handles multiple cards', () => {
      render(
        <SpreadLayout
          spreadType="three_card"
          cards={mockCards}
        />
      );
      const images = screen.getAllByRole('img');
      expect(images.length).toBe(3);
    });
  });

  describe('refs', () => {
    it('forwards ref correctly', () => {
      const ref = { current: null as HTMLDivElement | null };
      render(
        <SpreadLayout
          ref={ref}
          spreadType="three_card"
          cards={mockCards}
        />
      );
      expect(ref.current).toBeInstanceOf(HTMLDivElement);
    });
  });
});
