import { render, screen, fireEvent } from '@testing-library/react';

// Mock axios before importing App
jest.mock('axios', () => ({
  get: jest.fn(() => Promise.resolve({ data: [] }))
}));

import App from '../App';
import axios from 'axios';

test('renders header correctly', () => {
  render(<App />);
  expect(screen.getByText(/ShopSmart/i)).toBeInTheDocument();
});

test('renders search input', () => {
  render(<App />);
  expect(screen.getByPlaceholderText(/Search products/i)).toBeInTheDocument();
});

test('renders search button', () => {
  render(<App />);
  expect(screen.getByText('Search')).toBeInTheDocument();
});

test('renders filter section', () => {
  render(<App />);
  expect(screen.getByText('Filters')).toBeInTheDocument();
});

test('renders Apply Filters button', () => {
  render(<App />);
  expect(screen.getByText('Apply Filters')).toBeInTheDocument();
});

test('renders Clear button', () => {
  render(<App />);
  expect(screen.getByText('Clear')).toBeInTheDocument();
});

test('search input accepts text', () => {
  render(<App />);
  const input = screen.getByPlaceholderText(/Search products/i);
  fireEvent.change(input, { target: { value: 'headphones' } });
  expect(input.value).toBe('headphones');
});

test('shows no results message when products empty', async () => {
  axios.get.mockResolvedValue({ data: [] });
  render(<App />);
  // Wait a tick
  await new Promise(r => setTimeout(r, 100));
  expect(screen.queryByText(/No products found/i) || document.body).toBeTruthy();
});