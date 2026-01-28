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

// Base container interface
export interface BaseContainer {
  name?: string;
  widgets: WidgetSpec[];
  content?: Container[];
}

// Section container
export interface Section extends BaseContainer {
  type?: 'section';
}

// Tabs container
export interface Tab {
  name: string;
  widgets: WidgetSpec[];
  content?: Container[];
}

export interface TabsContainer extends BaseContainer {
  type: 'tabs';
  tabs: Tab[];
}

// Accordion container
export interface AccordionItem {
  name: string;
  widgets: WidgetSpec[];
  content?: Container[];
}

export interface AccordionContainer extends BaseContainer {
  type: 'accordion';
  items: AccordionItem[];
}

// Grid container
export interface GridColumn {
  widgets: WidgetSpec[];
  content?: Container[];
}

export interface GridRow {
  columns: GridColumn[];
}

export interface GridContainer extends BaseContainer {
  type: 'grid';
  rows: GridRow[];
}

// Union type for all container types
export type Container = Section | TabsContainer | AccordionContainer | GridContainer;

// Application specification
export interface AppSpec {
  name: string;
  description: string;
  functions: FunctionInfo[];
  function_groups?: Record<string, FunctionInfo[]>;
}

// Function group information
export interface FunctionGroup {
  name: string;
  functions: FunctionInfo[];
}

// Function output information
export interface FunctionOutput {
  name: string;
  type: string;
  description?: string;
}

// Function information
export interface FunctionInfo {
  name: string;
  display_name: string;
  description: string;
  outputs?: FunctionOutput[];
  layout: {
    sections?: Section[];
    containers: Container[];
  };
  group?: string;
}

// Run request
export interface RunRequest {
  func_name: string;
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

// Preset types
export interface Preset {
  id: string;
  name: string;
  description?: string;
  values: Record<string, any>;
  created_at: number;
  updated_at?: number;
}

export interface PresetCreate {
  name: string;
  description?: string;
  values: Record<string, any>;
}
