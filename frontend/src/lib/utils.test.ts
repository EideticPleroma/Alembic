import { describe, it, expect } from 'vitest';
import { cn } from './utils';

describe('cn', () => {
  it('merges multiple class names', () => {
    expect(cn('px-2', 'py-1')).toBe('px-2 py-1');
  });

  it('handles conditional classes with falsy values', () => {
    expect(cn('base', false && 'hidden', true && 'visible')).toBe(
      'base visible'
    );
  });

  it('handles undefined and null values', () => {
    expect(cn('px-2', undefined, null, 'py-1')).toBe('px-2 py-1');
  });

  it('deduplicates conflicting tailwind classes', () => {
    expect(cn('p-4', 'p-2')).toBe('p-2');
  });

  it('deduplicates padding classes from different directions', () => {
    expect(cn('px-4 py-2', 'px-2')).toBe('py-2 px-2');
  });

  it('handles array inputs', () => {
    expect(cn(['px-2', 'py-1'])).toBe('px-2 py-1');
  });

  it('handles object inputs with class-variance-authority style', () => {
    expect(cn('base', { 'text-gold': true, 'text-silver': false })).toBe(
      'base text-gold'
    );
  });

  it('returns empty string for empty input', () => {
    expect(cn()).toBe('');
  });

  it('handles hermetic color classes', () => {
    expect(cn('bg-void', 'text-gold', 'border-silver')).toBe(
      'bg-void text-gold border-silver'
    );
  });
});
