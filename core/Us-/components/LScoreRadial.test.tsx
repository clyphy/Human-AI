/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { describe, expect, test } from '@jest/globals';
import LScoreRadial from './LScoreRadial';

describe('LScoreRadial', () => {
  test('renders with correct score display', () => {
    render(<LScoreRadial score={75} />);
    
    expect(screen.getByText('75')).toBeInTheDocument();
    expect(screen.getByText('L-Score')).toBeInTheDocument();
  });

  test('clamps scores above 100 to 100', () => {
    render(<LScoreRadial score={150} />);
    
    expect(screen.getByText('100')).toBeInTheDocument();
  });

  test('clamps scores below 0 to 0', () => {
    render(<LScoreRadial score={-50} />);
    
    expect(screen.getByText('0')).toBeInTheDocument();
  });

  test('displays green color for scores >= 85', () => {
    render(<LScoreRadial score={90} />);
    
    const scoreElement = screen.getByText('90');
    expect(scoreElement).toHaveClass('text-green-400');
  });

  test('displays amber color for scores between 70 and 84', () => {
    render(<LScoreRadial score={75} />);
    
    const scoreElement = screen.getByText('75');
    expect(scoreElement).toHaveClass('text-amber-400');
  });

  test('displays red color for scores < 70', () => {
    render(<LScoreRadial score={65} />);
    
    const scoreElement = screen.getByText('65');
    expect(scoreElement).toHaveClass('text-red-500');
  });

  test('has proper accessibility attributes', () => {
    render(<LScoreRadial score={80} />);
    
    const progressBar = screen.getByRole('progressbar');
    expect(progressBar).toHaveAttribute('aria-valuenow', '80');
    expect(progressBar).toHaveAttribute('aria-valuemin', '0');
    expect(progressBar).toHaveAttribute('aria-valuemax', '100');
    expect(progressBar).toHaveAttribute('aria-label', 'L-Score: 80 out of 100');
  });

  test('handles decimal scores correctly', () => {
    render(<LScoreRadial score={87.5} />);
    
    expect(screen.getByText('88')).toBeInTheDocument();
  });
});
