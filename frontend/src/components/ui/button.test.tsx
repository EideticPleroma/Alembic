import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import { Button } from './button';

describe('Button', () => {
  it('renders with children text', () => {
    render(<Button>Click me</Button>);
    expect(
      screen.getByRole('button', { name: 'Click me' })
    ).toBeInTheDocument();
  });

  it('renders with default variant classes', () => {
    render(<Button>Default</Button>);
    const button = screen.getByRole('button');
    expect(button.className).toContain('bg-gold');
    expect(button.className).toContain('text-void');
  });

  it('applies correct classes for mystical variant', () => {
    render(<Button variant="mystical">Mystical</Button>);
    const button = screen.getByRole('button');
    expect(button.className).toContain('from-void');
    expect(button.className).toContain('to-midnight');
    expect(button.className).toContain('text-gold');
  });

  it('applies correct classes for outline variant', () => {
    render(<Button variant="outline">Outline</Button>);
    const button = screen.getByRole('button');
    expect(button.className).toContain('border');
    expect(button.className).toContain('border-gold');
    expect(button.className).toContain('text-gold');
  });

  it('applies correct size classes', () => {
    const { rerender } = render(<Button size="sm">Small</Button>);
    let button = screen.getByRole('button');
    expect(button.className).toContain('h-9');

    rerender(<Button size="lg">Large</Button>);
    button = screen.getByRole('button');
    expect(button.className).toContain('h-11');
  });

  it('applies disabled state', () => {
    render(<Button disabled>Disabled</Button>);
    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
  });

  it('supports custom className prop', () => {
    render(<Button className="custom-class">Custom</Button>);
    const button = screen.getByRole('button');
    expect(button.className).toContain('custom-class');
  });

  it('handles onClick events', async () => {
    const handleClick = vi.fn();
    const { container } = render(
      <Button onClick={handleClick}>Click</Button>
    );
    const button = container.querySelector('button') as HTMLButtonElement;
    button?.click();
    expect(handleClick).toHaveBeenCalled();
  });

  it('renders as child component when asChild is true', () => {
    render(
      <Button asChild>
        <a href="/test">Link Button</a>
      </Button>
    );
    const link = screen.getByRole('link');
    expect(link).toHaveAttribute('href', '/test');
  });

  it('forwards ref correctly', () => {
    const ref = { current: null as HTMLButtonElement | null };
    render(
      <Button ref={ref}>Ref test</Button>
    );
    expect(ref.current).toBeInstanceOf(HTMLButtonElement);
  });

  it('combines variant and size classes', () => {
    render(
      <Button variant="mystical" size="lg">
        Large Mystical
      </Button>
    );
    const button = screen.getByRole('button');
    expect(button.className).toContain('from-void');
    expect(button.className).toContain('h-11');
  });
});
