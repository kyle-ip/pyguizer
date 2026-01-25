/**
 * Integration tests for App component
 * Tests complete user flows and interactions
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';
import * as api from './services/api';

// Mock the API services
jest.mock('./services/api', () => ({
  getAppSpec: jest.fn(),
  runFunction: jest.fn(),
  getTask: jest.fn(),
  getFunctions: jest.fn(),
  getFunction: jest.fn(),
  getPresets: jest.fn(),
  createPreset: jest.fn(),
  deletePreset: jest.fn(),
  WebSocketManager: jest.fn(() => ({
    connect: jest.fn(),
    disconnect: jest.fn(),
    on: jest.fn(),
    off: jest.fn(),
    send: jest.fn()
  }))
}));

const mockAppSpec = {
  name: 'Test App',
  description: 'Test application',
  functions: [
    {
      name: 'add',
      display_name: 'Add',
      description: 'Add two numbers',
      layout: {
        containers: [
          {
            name: 'Main',
            type: 'section',
            widgets: [
              {
                id: 'a',
                label: 'A',
                type: 'number',
                default: 0,
                required: true,
                data_type: 'int',
                constraints: { integer: true }
              },
              {
                id: 'b',
                label: 'B',
                type: 'number',
                default: 0,
                required: true,
                data_type: 'int',
                constraints: { integer: true }
              }
            ]
          }
        ]
      }
    },
    {
      name: 'multiply',
      display_name: 'Multiply',
      description: 'Multiply two numbers',
      layout: {
        containers: [
          {
            name: 'Main',
            type: 'section',
            widgets: [
              {
                id: 'x',
                label: 'X',
                type: 'number',
                default: 1,
                required: true,
                data_type: 'float',
                constraints: {}
              },
              {
                id: 'y',
                label: 'Y',
                type: 'number',
                default: 1,
                required: true,
                data_type: 'float',
                constraints: {}
              }
            ]
          }
        ]
      }
    }
  ]
};

describe('App Integration Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (api.getAppSpec as jest.Mock).mockResolvedValue(mockAppSpec);
    (api.getPresets as jest.Mock).mockResolvedValue([]);
    (api.runFunction as jest.Mock).mockResolvedValue({
      task_id: 'test-task-123',
      status: 'pending'
    });
    (api.getTask as jest.Mock).mockResolvedValue({
      task_id: 'test-task-123',
      status: 'success',
      result: 8,
      created_at: Date.now(),
      completed_at: Date.now()
    });
  });

  describe('Multi-Function Flow', () => {
    it('should display function sidebar with all functions', async () => {
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Test App')).toBeInTheDocument();
      });

      expect(screen.getByText('Functions')).toBeInTheDocument();
      expect(screen.getByText('Add')).toBeInTheDocument();
      expect(screen.getByText('Multiply')).toBeInTheDocument();
    });

    it('should switch between functions when clicking sidebar', async () => {
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Add')).toBeInTheDocument();
      });

      // Initially, first function should be selected
      expect(screen.getByLabelText('A')).toBeInTheDocument();
      expect(screen.getByLabelText('B')).toBeInTheDocument();

      // Click on multiply function
      fireEvent.click(screen.getByText('Multiply'));

      // Should show multiply function inputs
      await waitFor(() => {
        expect(screen.getByLabelText('X')).toBeInTheDocument();
        expect(screen.getByLabelText('Y')).toBeInTheDocument();
      });
    });

    it('should execute selected function with correct inputs', async () => {
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Add')).toBeInTheDocument();
      });

      // Fill in inputs
      fireEvent.change(screen.getByLabelText('A'), { target: { value: '5' } });
      fireEvent.change(screen.getByLabelText('B'), { target: { value: '3' } });

      // Submit form
      fireEvent.click(screen.getByText('Run Function'));

      await waitFor(() => {
        expect(api.runFunction).toHaveBeenCalledWith('add', {
          a: 5,
          b: 3
        });
      });
    });
  });

  describe('Preset Management Flow', () => {
    it('should display presets section', async () => {
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Presets')).toBeInTheDocument();
      });
    });

    it('should create and save a preset', async () => {
      (api.createPreset as jest.Mock).mockResolvedValue({
        id: 'preset-1',
        name: 'Test Preset',
        values: { a: 5, b: 3 },
        created_at: Date.now()
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Add')).toBeInTheDocument();
      });

      // Fill in inputs
      fireEvent.change(screen.getByLabelText('A'), { target: { value: '5' } });
      fireEvent.change(screen.getByLabelText('B'), { target: { value: '3' } });

      // Click save preset button
      fireEvent.click(screen.getByText('Save Current Inputs as Preset'));

      // Fill in preset name
      await waitFor(() => {
        const nameInput = screen.getByPlaceholderText('Enter preset name');
        fireEvent.change(nameInput, { target: { value: 'Test Preset' } });
      });

      // Save preset
      fireEvent.click(screen.getByText('Save Preset'));

      await waitFor(() => {
        expect(api.createPreset).toHaveBeenCalledWith({
          name: 'Test Preset',
          description: '',
          values: { a: 5, b: 3 }
        });
      });
    });

    it('should load a preset', async () => {
      const mockPresets = [
        {
          id: 'preset-1',
          name: 'Saved Preset',
          values: { a: 10, b: 20 },
          created_at: Date.now()
        }
      ];

      (api.getPresets as jest.Mock).mockResolvedValue(mockPresets);

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Saved Preset')).toBeInTheDocument();
      });

      // Click load button
      const loadButtons = screen.getAllByText('Load');
      fireEvent.click(loadButtons[0]);

      // Check that inputs are populated
      await waitFor(() => {
        const aInput = screen.getByLabelText('A') as HTMLInputElement;
        expect(aInput.value).toBe('10');
      });
    });
  });

  describe('Task Execution Flow', () => {
    it('should show loading state during task execution', async () => {
      // Mock task in progress
      (api.getTask as jest.Mock)
        .mockResolvedValueOnce({
          task_id: 'test-task-123',
          status: 'running',
          progress: 0.5,
          message: 'Processing...'
        })
        .mockResolvedValueOnce({
          task_id: 'test-task-123',
          status: 'success',
          result: 8,
          progress: 1.0
        });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Add')).toBeInTheDocument();
      });

      // Submit form
      fireEvent.click(screen.getByText('Run Function'));

      // Should show loading state
      await waitFor(() => {
        expect(screen.getByText('Running...')).toBeInTheDocument();
      });
    });

    it('should display result after successful execution', async () => {
      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Add')).toBeInTheDocument();
      });

      // Submit form
      fireEvent.click(screen.getByText('Run Function'));

      // Should show result
      await waitFor(() => {
        expect(screen.getByText('Result')).toBeInTheDocument();
        expect(screen.getByText('8')).toBeInTheDocument();
      });
    });

    it('should display error on task failure', async () => {
      (api.getTask as jest.Mock).mockResolvedValue({
        task_id: 'test-task-123',
        status: 'failed',
        error: 'Division by zero',
        created_at: Date.now(),
        completed_at: Date.now()
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Add')).toBeInTheDocument();
      });

      // Submit form
      fireEvent.click(screen.getByText('Run Function'));

      // Should show error
      await waitFor(() => {
        expect(screen.getByText(/Division by zero/i)).toBeInTheDocument();
      });
    });
  });

  describe('Error Handling', () => {
    it('should handle API errors gracefully', async () => {
      (api.getAppSpec as jest.Mock).mockRejectedValue(new Error('Network Error'));

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText(/Failed to fetch application specification/i)).toBeInTheDocument();
      });
    });

    it('should handle function execution errors', async () => {
      (api.runFunction as jest.Mock).mockRejectedValue({
        response: {
          data: { detail: 'Invalid inputs' }
        }
      });

      render(<App />);

      await waitFor(() => {
        expect(screen.getByText('Add')).toBeInTheDocument();
      });

      // Submit form
      fireEvent.click(screen.getByText('Run Function'));

      await waitFor(() => {
        expect(screen.getByText(/Invalid inputs/i)).toBeInTheDocument();
      });
    });
  });
});
