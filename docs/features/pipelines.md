# Pipeline Support

PyGUIzer now includes powerful pipeline support, allowing you to create, configure, and execute directed acyclic graphs (DAGs) of functions.

## Overview

Pipelines enable you to:

- Create complex workflows by connecting multiple functions
- Run functions in serial or parallel execution modes
- Handle both synchronous and asynchronous functions
- Automatically manage dependencies between functions
- Visualize and manage workflows through a comprehensive API

## Core Concepts

### Pipeline
A pipeline is a collection of nodes and connections that form a directed acyclic graph (DAG).

### Node
A node represents a single function instance in the pipeline. Nodes can be:
- Synchronous or asynchronous functions
- Multiple instances of the same function
- Configured with default parameter values

### Connection
A connection links an output from one node to an input of another node, creating a dependency relationship.

## API Endpoints

### Pipeline Management

#### Create a Pipeline
```bash
POST /api/pipelines
```

**Request Body:**
```json
{
  "name": "My Pipeline",
  "description": "A test pipeline"
}
```

#### Get All Pipelines
```bash
GET /api/pipelines
```

#### Get a Specific Pipeline
```bash
GET /api/pipelines/{pipeline_id}
```

#### Update a Pipeline
```bash
PUT /api/pipelines/{pipeline_id}
```

**Request Body:**
```json
{
  "name": "Updated Pipeline",
  "description": "An updated pipeline"
}
```

#### Delete a Pipeline
```bash
DELETE /api/pipelines/{pipeline_id}
```

### Node Management

#### Add a Node
```bash
POST /api/pipelines/{pipeline_id}/nodes
```

**Request Body:**
```json
{
  "function_name": "add",
  "node_name": "Add Node",
  "parameters": {"a": 1, "b": 2},
  "position": {"x": 100, "y": 100}
}
```

#### Update a Node
```bash
PUT /api/pipelines/{pipeline_id}/nodes/{node_id}
```

**Request Body:**
```json
{
  "node_name": "Updated Add Node",
  "parameters": {"a": 5, "b": 5},
  "position": {"x": 150, "y": 100}
}
```

#### Delete a Node
```bash
DELETE /api/pipelines/{pipeline_id}/nodes/{node_id}
```

### Connection Management

#### Add a Connection
```bash
POST /api/pipelines/{pipeline_id}/connections
```

**Request Body:**
```json
{
  "source_node_id": "source-node-id",
  "source_output": "result",
  "target_node_id": "target-node-id",
  "target_input": "x"
}
```

#### Delete a Connection
```bash
DELETE /api/pipelines/{pipeline_id}/connections/{connection_id}
```

### Pipeline Execution

#### Validate a Pipeline
```bash
POST /api/pipelines/{pipeline_id}/validate
```

#### Execute a Pipeline
```bash
POST /api/pipelines/{pipeline_id}/execute
```

**Request Body:**
```json
{
  "execution_mode": "parallel",
  "run_async": true
}
```

## Execution Modes

### Serial Execution
Functions are executed in topological order, one after another. This mode is useful when functions have strict dependencies or when you want deterministic execution order.

### Parallel Execution
Independent functions are executed concurrently using `asyncio.gather()`. This mode significantly improves performance for pipelines with many independent functions.

## Example Workflow

### 1. Create a Pipeline
```bash
curl -X POST http://localhost:8000/api/pipelines \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Math Pipeline",
    "description": "A pipeline for mathematical operations"
  }'
```

### 2. Add Nodes

#### Add Add Node
```bash
curl -X POST http://localhost:8000/api/pipelines/{pipeline_id}/nodes \
  -H "Content-Type: application/json" \
  -d '{
    "function_name": "add",
    "node_name": "Add Numbers",
    "parameters": {"a": 1, "b": 2}
  }'
```

#### Add Multiply Node
```bash
curl -X POST http://localhost:8000/api/pipelines/{pipeline_id}/nodes \
  -H "Content-Type: application/json" \
  -d '{
    "function_name": "multiply",
    "node_name": "Multiply Result",
    "parameters": {"y": 2}
  }'
```

### 3. Add Connection
```bash
curl -X POST http://localhost:8000/api/pipelines/{pipeline_id}/connections \
  -H "Content-Type: application/json" \
  -d '{
    "source_node_id": "{add-node-id}",
    "source_output": "result",
    "target_node_id": "{multiply-node-id}",
    "target_input": "x"
  }'
```

### 4. Validate Pipeline
```bash
curl -X POST http://localhost:8000/api/pipelines/{pipeline_id}/validate
```

### 5. Execute Pipeline
```bash
curl -X POST http://localhost:8000/api/pipelines/{pipeline_id}/execute \
  -H "Content-Type: application/json" \
  -d '{
    "execution_mode": "parallel",
    "run_async": true
  }'
```

## Best Practices

### Pipeline Design

1. **Keep pipelines focused** - Create separate pipelines for different logical workflows
2. **Use meaningful node names** - Helps with visualization and debugging
3. **Limit pipeline complexity** - Break large pipelines into smaller, reusable components
4. **Test incrementally** - Build and test pipeline components individually before connecting them

### Performance Optimization

1. **Use parallel execution** for independent functions
2. **Prefer async functions** for I/O-bound operations
3. **Minimize data transfer** between nodes
4. **Monitor pipeline execution** to identify bottlenecks

### Error Handling

1. **Validate pipelines before execution**
2. **Implement error handling in functions**
3. **Use appropriate timeouts** for long-running operations
4. **Monitor execution status** through WebSocket updates

## Integration with Frontend

The pipeline API is designed to be easily integrated with frontend applications. Key features for frontend integration include:

- **Comprehensive CRUD operations** for all pipeline components
- **Real-time execution status** via WebSockets
- **Position data** for node layout in visual editors
- **Detailed validation feedback** for user guidance
- **Execution metrics** for performance monitoring

## Future Enhancements

Planned pipeline enhancements include:

- **Pipeline templates** for reusable workflow patterns
- **Parameter sweep** functionality for batch processing
- **Conditional execution** based on function results
- **Persistent storage** for pipelines
- **Version control** for pipeline configurations
- **Advanced visualization tools** for complex pipelines
