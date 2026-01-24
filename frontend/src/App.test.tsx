import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';
import * as api from './services/api';

// Mock the API services
jest.mock('./services/api', () => ({
  getAppSpec: jest.fn(),
  runFunction: jest.fn(),
  getTask: jest.fn(),
  WebSocketManager: jest.fn(() => ({
    connect: jest.fn(),
    disconnect: jest.fn(),
    on: jest.fn(),
    off: jest.fn(),
    send: jest.fn()
  }))
}));

// Mock app specification data
const mockAppSpec = {
  name: 'Test App',
  description: 'Test application description',
  layout: {
    sections: [
      {
        name: 'Main',
        widgets: [
          {
            id: 'test_text',
            label: 'Test Text',
            type: 'text',
            default: 'default_value',
            required: true,
            data_type: 'str',
            constraints: {}
          },
          {
            id: 'test_number',
            label: 'Test Number',
            type: 'number',
            default: 42,
            required: true,
            data_type: 'int',
            constraints: { integer: true }
          },
          {
            id: 'test_boolean',
            label: 'Test Boolean',
            type: 'boolean',
            default: true,
            required: false,
            data_type: 'bool',
            constraints: {}
          }
        ]
      }
    ]
  }
};

describe('App Component', () => {
  beforeEach(() => {
    // Reset all mocks before each test
    jest.clearAllMocks();
    
    // Mock getAppSpec to return our mock data
    (api.getAppSpec as jest.Mock).mockResolvedValue(mockAppSpec);
    
    // Mock runFunction to return a task ID
    (api.runFunction as jest.Mock).mockResolvedValue({
      task_id: 'test-task-123',
      status: 'pending'
    });
    
    // Mock getTask to return task status
    (api.getTask as jest.Mock).mockResolvedValue({
      task_id: 'test-task-123',
      status: 'success',
      created_at: Date.now(),
      completed_at: Date.now(),
      result: 'Test result',
      progress: 1.0,
      message: 'Task completed'
    });
  });

  test('renders without throwing invalid hook call errors', async () => {
    // This test ensures no invalid hook calls occur
    expect(() => {
      render(<App />);
    }).not.toThrow();
  });

  test('renders the app with correct structure', async () => {
    render(<App />);
    
    // Wait for the app to load
    await waitFor(() => {
      expect(screen.getByText('Test App')).toBeInTheDocument();
    });
    
    // Check that sections and widgets render
    expect(screen.getByText('Main')).toBeInTheDocument();
    expect(screen.getByLabelText('Test Text')).toBeInTheDocument();
    expect(screen.getByLabelText('Test Number')).toBeInTheDocument();
    expect(screen.getByLabelText('Test Boolean')).toBeInTheDocument();
    
    // Check that the run button renders
    expect(screen.getByText('Run Function')).toBeInTheDocument();
  });

  test('submits form correctly', async () => {
    render(<App />);
    
    // Wait for the app to load
    await waitFor(() => {
      expect(screen.getByText('Test App')).toBeInTheDocument();
    });
    
    // Fill in form values
    fireEvent.change(screen.getByLabelText('Test Text'), { target: { value: 'new_value' } });
    fireEvent.change(screen.getByLabelText('Test Number'), { target: { value: '100' } });
    fireEvent.click(screen.getByLabelText('Test Boolean'));
    
    // Submit the form
    fireEvent.click(screen.getByText('Run Function'));
    
    // Check that runFunction was called with correct inputs
    await waitFor(() => {
      expect(api.runFunction).toHaveBeenCalledWith({
        test_text: 'new_value',
        test_number: 100,
        test_boolean: false
      });
    });
  });

  test('handles task updates correctly', async () => {
    render(<App />);
    
    // Wait for the app to load
    await waitFor(() => {
      expect(screen.getByText('Test App')).toBeInTheDocument();
    });
    
    // Submit the form
    fireEvent.click(screen.getByText('Run Function'));
    
    // Check that getTask is called
    await waitFor(() => {
      expect(api.getTask).toHaveBeenCalledWith('test-task-123');
    });
  });

  test('initializes WebSocket manager correctly', async () => {
    render(<App />);
    
    // Wait for the app to load
    await waitFor(() => {
      expect(screen.getByText('Test App')).toBeInTheDocument();
    });
    
    // Submit the form
    fireEvent.click(screen.getByText('Run Function'));
    
    // Check that WebSocketManager was instantiated
    await waitFor(() => {
      expect(api.WebSocketManager).toHaveBeenCalled();
    });
  });

  test('displays error messages when API fails', async () => {
    // Mock getAppSpec to reject
    (api.getAppSpec as jest.Mock).mockRejectedValue(new Error('API Error'));
    
    render(<App />);
    
    // Check that error message is displayed
    await waitFor(() => {
      expect(screen.getByText('Failed to fetch application specification')).toBeInTheDocument();
    });
  });
});
