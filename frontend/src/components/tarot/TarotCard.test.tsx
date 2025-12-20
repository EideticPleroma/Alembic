import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import { TarotCard } from './TarotCard';

describe('TarotCard', () => {
  const mockCard = {
    id: 'major_00',
    name: 'The Fool',
    image_url: '/cards/major_00.png',
  };

  describe('rendering', () => {
    it('renders card name', () => {
      render(<TarotCard card={mockCard} />);
      expect(screen.getByText('The Fool')).toBeInTheDocument();
    });

    it('renders position when provided', () => {
      render(<TarotCard card={mockCard} position="Past" />);
      expect(screen.getByText('Past')).toBeInTheDocument();
    });

    it('does not render position when not provided', () => {
      render(<TarotCard card={mockCard} />);
      expect(screen.queryByText(/Past|Present|Future/)).not.toBeInTheDocument();
    });

    it('renders card image', () => {
      render(<TarotCard card={mockCard} />);
      const img = screen.getByAltText('The Fool');
      expect(img).toBeInTheDocument();
      expect(img).toHaveAttribute('src', '/cards/major_00.png');
    });
  });

  describe('reversal state', () => {
    it('shows reversal indicator when reversed', () => {
      render(<TarotCard card={mockCard} isReversed={true} />);
      expect(screen.getByText('Rev.')).toBeInTheDocument();
    });

    it('does not show reversal indicator when not reversed', () => {
      render(<TarotCard card={mockCard} isReversed={false} />);
      expect(screen.queryByText('Rev.')).not.toBeInTheDocument();
    });

    it('applies reversed rotation class when reversed', () => {
      const { container } = render(
        <TarotCard card={mockCard} isReversed={true} />
      );
      const cardContent = container.querySelector('.rotate-180');
      expect(cardContent).toBeInTheDocument();
    });
  });

  describe('revealed state', () => {
    it('shows card content when revealed', () => {
      render(<TarotCard card={mockCard} isRevealed={true} />);
      expect(screen.getByText('The Fool')).toBeInTheDocument();
      expect(screen.getByAltText('The Fool')).toBeInTheDocument();
    });

    it('shows unrevealed state when not revealed', () => {
      render(<TarotCard card={mockCard} isRevealed={false} />);
      expect(screen.getByText('Unrevealed')).toBeInTheDocument();
      expect(screen.queryByText('The Fool')).not.toBeInTheDocument();
    });
  });

  describe('interactions', () => {
    it('calls onClick when clicked', () => {
      const handleClick = vi.fn();
      const { container } = render(
        <TarotCard card={mockCard} onClick={handleClick} />
      );
      const root = container.firstChild as HTMLElement;
      root.click();
      expect(handleClick).toHaveBeenCalled();
    });

    it('forwards ref correctly', () => {
      const ref = { current: null as HTMLDivElement | null };
      render(<TarotCard card={mockCard} ref={ref} />);
      expect(ref.current).toBeInstanceOf(HTMLDivElement);
    });
  });

  describe('defaults', () => {
    it('uses default isReversed as false', () => {
      render(<TarotCard card={mockCard} />);
      expect(screen.queryByText('Rev.')).not.toBeInTheDocument();
    });

    it('uses default isRevealed as true', () => {
      render(<TarotCard card={mockCard} />);
      expect(screen.getByText('The Fool')).toBeInTheDocument();
    });
  });
});
