// Widget specification
export interface WidgetSpec {
  id: string;
  label: string;
  type: string;
  default: any;
  required: boolean;
  data_type: string;
  constraints: {
    [key: string]: any;
  };
}

// Section definition
export interface Section {
  name: string;
  widgets: WidgetSpec[];
}

// Application specification
export interface AppSpec {
  name: string;
  description: string;
  layout: {
    sections: Section[];
  };
}

// Run request
export interface RunRequest {
  inputs: Record<string, any>;
}

// Task status
export enum TaskStatus {
  PENDING = "pending",
  RUNNING = "running",
  STREAMING = "streaming",
  SUCCESS = "success",
  FAILED = "failed",
  CANCELLED = "cancelled"
}

// Run response
export interface RunResponse {
  task_id: string;
  status: TaskStatus;
}

// Task info
export interface TaskInfo {
  task_id: string;
  status: TaskStatus;
  created_at: number;
  started_at?: number;
  completed_at?: number;
  result?: any;
  error?: string;
  progress?: number;
  message?: string;
}

// Extended widget types
export enum WidgetType {
  TEXT = "text",
  NUMBER = "number",
  SLIDER = "slider",
  BOOLEAN = "boolean",
  MULTI_SELECT = "multi_select",
  SELECT = "select",
  JSON = "json",
  FILE_UPLOAD = "file_upload",
  DATE = "date",
  TIME = "time",
  DATETIME = "datetime",
  COLOR = "color"
}