# API Documentation

PyGUIzer provides a comprehensive API for both backend and frontend interactions. This document describes the available endpoints and how to use them.

## Backend API

### FastAPI Application

PyGUIzer uses FastAPI for its backend, providing automatic API documentation at `/docs` when the server is running.

### Main Endpoints

#### GET /

Serves the main React frontend application.

#### GET /api/functions

Returns a list of all registered functions with their signatures and metadata.

**Response:**
```json
[
  {
    "name": "add",
    "description": "Add two numbers together.",
    "parameters": [
      {
        "name": "a",
        "type": "int",
        "default": null,
        "required": true
      },
      {
        "name": "b",
        "type": "int",
        "default": null,
        "required": true
      }
    ],
    "return_type": "int"
  }
]
```

#### POST /api/functions/{function_name}

Executes the specified function with the provided parameters.

**Request Body:**
```json
{
  "parameters": {
    "a": 5,
    "b": 10
  }
}
```

**Response:**
```json
{
  "result": 15,
  "execution_time": 0.001,
  "success": true
}
```

#### POST /api/run

Executes a function asynchronously with task tracking.

**Request Body:**
```json
{
  "func_name": "sync_function",
  "inputs": {
    "x": 10,
    "y": 20
  }
}
```

**Response:**
```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "pending"
}
```

#### GET /api/tasks/{task_id}

Gets the status and result of a task.

**Response:**
```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "success",
  "created_at": 1620000000.0,
  "started_at": 1620000000.1,
  "completed_at": 1620000001.2,
  "result": 30,
  "progress": 1.0,
  "message": "Task completed successfully"
}
```

#### POST /api/batch

Executes multiple functions in batch mode concurrently.

**Request Body:**
```json
{
  "functions": [
    {
      "name": "add",
      "inputs": {
        "a": 5,
        "b": 10
      }
    },
    {
      "name": "greet",
      "inputs": {
        "name": "World",
        "age": 30
      }
    }
  ]
}
```

**Response:**
```json
{
  "batch_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "running"
}
```

### WebSocket Endpoints

#### WS /ws

Provides real-time communication for task updates and bidirectional messaging.

**Message Types:**
- `task_update`: Updates on task progress and status
- `preset_change`: Notifications about preset changes
- `error`: Error messages from the server
- `success`: Success messages from the server

## Frontend API

### React Components

#### WidgetFactory

The `WidgetFactory` component is responsible for generating UI widgets based on Python types:

```tsx
import { WidgetFactory } from './components/WidgetFactory';

<WidgetFactory
  widget={widgetSpec}
  value={currentValue}
  onChange={handleChange}
  disabled={isDisabled}
/>
```

#### LayoutEditor

The `LayoutEditor` component provides drag-and-drop functionality for custom layouts:

```tsx
import { LayoutEditor } from './components/LayoutEditor';

<LayoutEditor
  widgets={widgets}
  layout={currentLayout}
  onChange={handleLayoutChange}
/>
```

#### Chart

The `Chart` component provides data visualization using Chart.js:

```tsx
import { Chart } from './components/Chart';

<Chart
  data={chartData}
  type="line"
  options={chartOptions}
/>
```

### Services

#### ApiService

The `ApiService` class handles communication with the backend API:

```ts
import { ApiService } from './services/api';

const api = new ApiService();

// Execute a function
const result = await api.executeFunction('add', { a: 5, b: 10 });

// Get function list
const functions = await api.getFunctions();

// Execute batch operations
const batchResult = await api.executeBatch([
  { name: 'add', parameters: { a: 5, b: 10 } },
  { name: 'greet', parameters: { name: 'World', age: 30 } }
]);
```

#### WebSocketService

The `WebSocketService` class handles real-time communication:

```ts
import { WebSocketService } from './services/websocket';

const ws = new WebSocketService();

// Connect to WebSocket
ws.connect();

// Listen for task updates
ws.on('task_update', (data) => {
  console.log('Task update:', data);
});

// Send a message
ws.send({ type: 'preset_load', data: { presetId: '123' } });

// Disconnect
ws.disconnect();
```

## Customization API

### Widget Registry

The widget registry allows you to register custom mappings for Python types:

```python
from pyguizer.core.widget import register_widget_mapping, WidgetType

# Register a custom widget mapping
def custom_widget_generator(py_type):
    return WidgetType.TEXT, {"description": "Custom widget"}

register_widget_mapping(MyCustomType, custom_widget_generator, priority=10)
```

## Async and Concurrent Support

### Backend Implementation

PyGUIzer's backend API now supports both sync and async functions:

```python
# Async function execution flow
async def run_function(self, func_name: str, inputs: Dict[str, Any]) -> Any:
    """Run a registered function with provided inputs."""
    func = self.function_registry[func_name]["func"]
    
    # Check if the function is async
    if asyncio.iscoroutinefunction(func):
        return await func(**inputs)
    else:
        # Run sync function in executor
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: func(**inputs))

# Concurrent batch processing
async def run_batch(request: BatchRequest):
    """Run multiple functions in batch."""
    # Create tasks for each function
    async def process_function(i, func_data):
        # Process single function
        pass
    
    # Run all tasks concurrently
    tasks = [process_function(i, func_data) for i, func_data in enumerate(functions)]
    function_results = await asyncio.gather(*tasks)
```

### Key Benefits

- **Automatic detection**: The system automatically detects if a function is async or sync
- **Optimal execution**: Async functions are awaited directly, sync functions run in executors
- **Concurrent processing**: Batch requests are processed in parallel
- **Backward compatibility**: Existing sync functions continue to work unchanged

### Best Practices

1. **Use async functions** for I/O-bound operations (network calls, file I/O, etc.)
2. **Use sync functions** for CPU-bound operations (mathematical calculations, etc.)
3. **Leverage batch requests** for multiple related operations to take advantage of concurrency
4. **Monitor resource usage** when processing large batches to avoid overwhelming the system

## Customization API

### Layout Configuration

You can customize the UI layout using a configuration object:

```python
from pyguizer import PyGUIzer

layout = {
  "sections": [
    {
      "name": "Personal Info",
      "widgets": ["name", "age"]
    },
    {
      "name": "Preferences",
      "widgets": ["hobbies", "is_active"]
    }
  ]
}

app = PyGUIzer(layout=layout)

@app
def user_profile(name: str, age: int, hobbies: list, is_active: bool = True):
    # Function implementation
    pass
```

## CLI API

### Main Commands

#### run

Runs a PyGUIzer application from a Python file:

```bash
python -m pyguizer run app.py [--host HOST] [--port PORT]
```

#### package

Packages a PyGUIzer application into a standalone executable:

```bash
python -m pyguizer package app.py [--name NAME] [--output_dir OUTPUT_DIR] [--onefile] [--windowed]
```

#### version

Shows the current PyGUIzer version:

```bash
python -m pyguizer --version
```

## Environment Variables

PyGUIzer supports the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `PYTHONUNBUFFERED` | Disable output buffering | `1` |
| `PYGUIZER_HOST` | Host to bind the server | `0.0.0.0` |
| `PYGUIZER_PORT` | Port to bind the server | `8000` |
| `PYGUIZER_TITLE` | Application title | `PyGUIzer App` |
