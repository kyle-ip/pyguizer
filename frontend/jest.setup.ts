import '@testing-library/jest-dom';

// Mock window.fetch for API tests
global.fetch = jest.fn();

// Mock console.error to fail tests when there are errors
const originalError = console.error;
console.error = (...args) => {
  originalError(...args);
  throw new Error(`console.error was called with: ${args.join(' ')}`);
};
