import axios from 'axios';
import { AppSpec, RunRequest, RunResponse } from '../types';

const API_BASE_URL = '/api';

// Create axios instance with base URL
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Get application specification
export const getAppSpec = async (): Promise<AppSpec> => {
  const response = await api.get('/spec');
  return response.data;
};

// Run the function with provided inputs
export const runFunction = async (inputs: Record<string, any>): Promise<RunResponse> => {
  const request: RunRequest = { inputs };
  const response = await api.post('/run', request);
  return response.data;
};
