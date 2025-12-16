import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from './card';

describe('Card', () => {
  it('renders card container', () => {
    const { container: cardContainer } = render(
      <Card>
        <div>Content</div>
      </Card>
    );
    const cardElement = cardContainer.querySelector('[class*="rounded-lg"]');
    expect(cardElement).toBeInTheDocument();
  });

  it('applies Hermetic styling classes', () => {
    const { container: cardContainer } = render(
      <Card>
        <div>Content</div>
      </Card>
    );
    const card = cardContainer.firstChild as HTMLElement;
    expect(card.className).toContain('rounded-lg');
    expect(card.className).toContain('border');
    expect(card.className).toContain('border-gold');
  });

  it('CardHeader renders children', () => {
    render(
      <Card>
        <CardHeader>Header Content</CardHeader>
      </Card>
    );
    expect(screen.getByText('Header Content')).toBeInTheDocument();
  });

  it('CardTitle applies serif font and gold color', () => {
    render(
      <Card>
        <CardHeader>
          <CardTitle>Test Title</CardTitle>
        </CardHeader>
      </Card>
    );
    const title = screen.getByText('Test Title');
    expect(title.className).toContain('font-serif');
    expect(title.className).toContain('text-gold');
  });

  it('CardDescription applies silver color', () => {
    render(
      <Card>
        <CardHeader>
          <CardDescription>Test Description</CardDescription>
        </CardHeader>
      </Card>
    );
    const description = screen.getByText('Test Description');
    expect(description.className).toContain('text-silver');
  });

  it('CardContent renders with correct padding', () => {
    render(
      <Card>
        <CardContent>Content</CardContent>
      </Card>
    );
    const content = screen.getByText('Content');
    expect(content.className).toContain('p-6');
  });

  it('CardFooter renders children', () => {
    render(
      <Card>
        <CardFooter>Footer Content</CardFooter>
      </Card>
    );
    expect(screen.getByText('Footer Content')).toBeInTheDocument();
  });

  it('renders complete card structure', () => {
    render(
      <Card>
        <CardHeader>
          <CardTitle>Card Title</CardTitle>
          <CardDescription>Card Description</CardDescription>
        </CardHeader>
        <CardContent>Main content here</CardContent>
        <CardFooter>Footer</CardFooter>
      </Card>
    );

    expect(screen.getByText('Card Title')).toBeInTheDocument();
    expect(screen.getByText('Card Description')).toBeInTheDocument();
    expect(screen.getByText('Main content here')).toBeInTheDocument();
    expect(screen.getByText('Footer')).toBeInTheDocument();
  });

  it('supports custom className on Card', () => {
    const { container: cardContainer } = render(
      <Card className="custom-card">Content</Card>
    );
    const card = cardContainer.firstChild as HTMLElement;
    expect(card.className).toContain('custom-card');
  });

  it('supports custom className on CardTitle', () => {
    render(
      <Card>
        <CardHeader>
          <CardTitle className="custom-title">Title</CardTitle>
        </CardHeader>
      </Card>
    );
    const title = screen.getByText('Title');
    expect(title.className).toContain('custom-title');
  });
});
