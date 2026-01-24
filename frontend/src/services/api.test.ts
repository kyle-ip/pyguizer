// Unit tests for API service functionality.

import axios from 'axios';
import { getAppSpec, runFunction } from './api';
import { AppSpec as AppSpecType } from '../types';

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

// Mock the axios.create() result
const mockAxiosInstance = {
  get: jest.fn(),
  post: jest.fn(),
} as any;

mockedAxios.create.mockReturnValue(mockAxiosInstance);

describe('API Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getAppSpec', () => {
    it('should fetch application specification successfully', async () => {
      const mockSpec: AppSpecType = {
        name: 'sample_function',
        description: 'Sample function for testing',
        sections: [
          {
            name: 'Main',
            widgets: [
              {
                id: 'name',
                label: 'Name',
                type: 'text',
                default: '',
                required: true,
                data_type: 'string',
                constraints: {}
              }
            ]
          }
        ]
      };

      mockAxiosInstance.get.mockResolvedValue({
        data: mockSpec
      });

      const result = await getAppSpec();

      expect(mockAxiosInstance.get).toHaveBeenCalledWith('/spec');
      expect(result).toEqual(mockSpec);
    });

    it('should throw an error when fetching app spec fails', async () => {
      mockAxiosInstance.get.mockRejectedValue({
        response: {
          status: 500,
          statusText: 'Internal Server Error'
        }
      });

      await expect(getAppSpec()).rejects.toThrow();
    });

    it('should throw an error when network request fails', async () => {
      mockAxiosInstance.get.mockRejectedValue(new Error('Network Error'));

      await expect(getAppSpec()).rejects.toThrow('Network Error');
    });
  });

  describe('runFunction', () => {
    it('should run function successfully with inputs', async () => {
      const mockInputs = { name: 'John', age: 30 };
      const mockResult = {
        result: 'Hello John, you are 30 years old.',
        execution_time: 0.01
      };

      mockAxiosInstance.post.mockResolvedValue({
        data: mockResult
      });

      const result = await runFunction(mockInputs);

      expect(mockAxiosInstance.post).toHaveBeenCalledWith('/run', { inputs: mockInputs });
      expect(result).toEqual(mockResult);
    });

    it('should handle empty inputs correctly', async () => {
      const mockInputs = {};
      const mockResult = {
        result: 'Default result',
        execution_time: 0.005
      };

      mockAxiosInstance.post.mockResolvedValue({
        data: mockResult
      });

      const result = await runFunction(mockInputs);

      expect(mockAxiosInstance.post).toHaveBeenCalledWith('/run', { inputs: mockInputs });
      expect(result).toEqual(mockResult);
    });

    it('should throw an error when function execution fails', async () => {
      const mockInputs = { name: 'John', age: 'invalid' };
      const errorMessage = 'TypeError: cannot convert string to int';

      mockAxiosInstance.post.mockRejectedValue({
        response: {
          status: 500,
          data: { detail: errorMessage }
        }
      });

      await expect(runFunction(mockInputs)).rejects.toThrow();
    });

    it('should throw an error when network request fails', async () => {
      const mockInputs = { name: 'John' };

      mockAxiosInstance.post.mockRejectedValue(new Error('Network Error'));

      await expect(runFunction(mockInputs)).rejects.toThrow('Network Error');
    });
  });
});
