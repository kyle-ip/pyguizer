// Widget types
export enum WidgetType {
  TEXT = "text",
  NUMBER = "number",
  SLIDER = "slider",
  BOOLEAN = "boolean",
  MULTI_SELECT = "multi_select",
  SELECT = "select",
  JSON = "json"
}

// Widget Specification Object (WSO)
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

// Run response
export interface RunResponse {
  result: any;
  execution_time: number;
}
