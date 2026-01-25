import axios from 'axios';
import {
  AppSpec, 
  RunRequest, 
  RunResponse, 
  TaskInfo,
  FunctionInfo
} from '../types/index';

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
export const runFunction = async (funcName: string, inputs: Record<string, any>): Promise<RunResponse> => {
  const request: RunRequest = { func_name: funcName, inputs };
  const response = await api.post('/run', request);
  return response.data;
};

// Get all registered functions
export const getFunctions = async (): Promise<FunctionInfo[]> => {
  const response = await api.get('/functions');
  return response.data;
};

// Get a specific function
export const getFunction = async (funcName: string): Promise<FunctionInfo> => {
  const response = await api.get(`/functions/${funcName}`);
  return response.data;
};

// Get task information
export const getTask = async (taskId: string): Promise<TaskInfo> => {
  const response = await api.get(`/tasks/${taskId}`);
  return response.data;
};

// Cancel a task
export const cancelTask = async (taskId: string): Promise<void> => {
  await api.post(`/tasks/${taskId}/cancel`);
};

// Preset management
export interface Preset {
  id: string;
  name: string;
  description: string;
  values: Record<string, any>;
  created_at: number;
  updated_at?: number;
}

export interface PresetCreate {
  name: string;
  description: string;
  values: Record<string, any>;
}

export interface PresetUpdate {
  name?: string;
  description?: string;
  values?: Record<string, any>;
}

// Get all presets
export const getPresets = async (): Promise<Preset[]> => {
  const response = await api.get('/presets');
  return response.data;
};

// Create a new preset
export const createPreset = async (preset: PresetCreate): Promise<Preset> => {
  const response = await api.post('/presets', preset);
  return response.data;
};

// Get a preset by ID
export const getPreset = async (presetId: string): Promise<Preset> => {
  const response = await api.get(`/presets/${presetId}`);
  return response.data;
};

// Update a preset
export const updatePreset = async (presetId: string, preset: PresetUpdate): Promise<Preset> => {
  const response = await api.put(`/presets/${presetId}`, preset);
  return response.data;
};

// Delete a preset
export const deletePreset = async (presetId: string): Promise<void> => {
  await api.delete(`/presets/${presetId}`);
};

// WebSocket manager for real-time updates
export class WebSocketManager {
  private ws: WebSocket | null = null;
  private listeners: Map<string, Array<(data: any) => void>> = new Map();

  connect(taskId: string): void {
    try {
      // Close existing connection if any
      if (this.ws) {
        this.ws.close();
      }

      // Open new WebSocket connection
      const wsUrl = `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/api/tasks/${taskId}/stream`;
      this.ws = new WebSocket(wsUrl);

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          const eventType = data.type;
          
          if (this.listeners.has(eventType)) {
            this.listeners.get(eventType)?.forEach(listener => {
              try {
                listener(data);
              } catch (error) {
                console.error('Error in WebSocket listener:', error);
              }
            });
          }
        } catch (error) {
          console.error('Error processing WebSocket message:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      this.ws.onclose = () => {
        console.log('WebSocket connection closed');
        this.ws = null;
      };
    } catch (error) {
      console.error('Error connecting WebSocket:', error);
    }
  }

  disconnect(): void {
    try {
      if (this.ws) {
        this.ws.close();
        this.ws = null;
      }
    } catch (error) {
      console.error('Error disconnecting WebSocket:', error);
    }
  }

  on(eventType: string, listener: (data: any) => void): void {
    if (!this.listeners.has(eventType)) {
      this.listeners.set(eventType, []);
    }
    this.listeners.get(eventType)?.push(listener);
  }

  off(eventType: string, listener: (data: any) => void): void {
    if (this.listeners.has(eventType)) {
      const listeners = this.listeners.get(eventType)?.filter(l => l !== listener);
      if (listeners?.length) {
        this.listeners.set(eventType, listeners);
      } else {
        this.listeners.delete(eventType);
      }
    }
  }

  send(data: any): void {
    try {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify(data));
      }
    } catch (error) {
      console.error('Error sending WebSocket message:', error);
    }
  }
}
