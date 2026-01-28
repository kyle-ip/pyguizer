"""API Examples for PyGUIzer"""

from typing import Any, Dict

# Function Execution Examples
RUN_EXAMPLES: Dict[str, Dict[str, Any]] = {
    "AddNumbers": {
        "summary": "Add Two Numbers",
        "description": "Run the add function with two numbers",
        "value": {"func_name": "add", "inputs": {"a": 5, "b": 3}},
    },
    "MultiplyNumbers": {
        "summary": "Multiply Two Numbers",
        "description": "Run the multiply function with two numbers",
        "value": {"func_name": "multiply", "inputs": {"x": 4, "y": 6}},
    },
    "AsyncAdd": {
        "summary": "Async Add Numbers",
        "description": "Run an async add function",
        "value": {"func_name": "async_add", "inputs": {"a": 10, "b": 20}},
    },
}

# Batch Processing Examples
BATCH_EXAMPLES: Dict[str, Dict[str, Any]] = {
    "MultipleSyncFunctions": {
        "summary": "Multiple Sync Functions",
        "description": "Run multiple sync functions in batch",
        "value": {
            "functions": [
                {"name": "add", "inputs": {"a": 1, "b": 2}},
                {"name": "multiply", "inputs": {"x": 3, "y": 4}},
                {"name": "add", "inputs": {"a": 10, "b": 20}},
            ]
        },
    },
    "MixedSyncAsync": {
        "summary": "Mixed Sync and Async Functions",
        "description": "Run a mix of sync and async functions",
        "value": {
            "functions": [
                {"name": "add", "inputs": {"a": 5, "b": 5}},
                {"name": "async_add", "inputs": {"a": 10, "b": 10}},
                {"name": "async_multiply", "inputs": {"x": 2, "y": 3}},
            ]
        },
    },
}

# Preset Examples
PRESET_EXAMPLES: Dict[str, Dict[str, Any]] = {
    "AddPreset": {
        "summary": "Add Function Preset",
        "description": "Preset for add function with specific values",
        "value": {
            "name": "Add 10 and 20",
            "description": "Adds 10 and 20",
            "values": {"a": 10, "b": 20},
        },
    },
    "MultiplyPreset": {
        "summary": "Multiply Function Preset",
        "description": "Preset for multiply function with specific values",
        "value": {
            "name": "Multiply by 5",
            "description": "Multiplies input by 5",
            "values": {"x": 10, "y": 5},
        },
    },
}

# Pipeline Examples
PIPELINE_EXAMPLES: Dict[str, Dict[str, Any]] = {
    "BasicPipeline": {
        "summary": "Basic Pipeline",
        "description": "Create a simple pipeline with two nodes",
        "value": {
            "name": "Basic Math Pipeline",
            "description": "A simple pipeline that adds and multiplies numbers",
        },
    },
    "ComplexPipeline": {
        "summary": "Complex Pipeline",
        "description": "Create a more complex pipeline",
        "value": {
            "name": "Data Processing Pipeline",
            "description": "Process data through multiple steps",
        },
    },
}

# Pipeline Node Examples
PIPELINE_NODE_EXAMPLES: Dict[str, Dict[str, Any]] = {
    "AddNode": {
        "summary": "Add Function Node",
        "description": "Add an add function node to a pipeline",
        "value": {
            "function_name": "add",
            "node_name": "Add Numbers",
            "parameters": {"a": 10, "b": 20},
            "position": {"x": 100, "y": 100},
        },
    },
    "MultiplyNode": {
        "summary": "Multiply Function Node",
        "description": "Add a multiply function node to a pipeline",
        "value": {
            "function_name": "multiply",
            "node_name": "Multiply Result",
            "parameters": {"y": 2},
            "position": {"x": 300, "y": 100},
        },
    },
    "AsyncAddNode": {
        "summary": "Async Add Function Node",
        "description": "Add an async add function node to a pipeline",
        "value": {
            "function_name": "async_add",
            "node_name": "Async Add",
            "parameters": {"a": 5, "b": 5},
            "position": {"x": 100, "y": 200},
        },
    },
}

# Pipeline Connection Examples
PIPELINE_CONNECTION_EXAMPLES: Dict[str, Dict[str, Any]] = {
    "BasicConnection": {
        "summary": "Basic Node Connection",
        "description": "Connect two nodes in a pipeline",
        "value": {
            "source_node_id": "source-node-id",
            "source_output": "result",
            "target_node_id": "target-node-id",
            "target_input": "x",
        },
    },
    "MultiInputConnection": {
        "summary": "Multiple Input Connection",
        "description": "Connect to multiple inputs of a node",
        "value": {
            "source_node_id": "another-source-id",
            "source_output": "result",
            "target_node_id": "target-node-id",
            "target_input": "y",
        },
    },
}

# Pipeline Execution Examples
PIPELINE_EXECUTION_EXAMPLES: Dict[str, Dict[str, Any]] = {
    "SerialExecution": {
        "summary": "Serial Execution",
        "description": "Execute pipeline in serial mode",
        "value": {"execution_mode": "serial", "run_async": True},
    },
    "ParallelExecution": {
        "summary": "Parallel Execution",
        "description": "Execute pipeline in parallel mode",
        "value": {"execution_mode": "parallel", "run_async": True},
    },
}

# Task Examples
TASK_EXAMPLES: Dict[str, Dict[str, Any]] = {
    "GetTaskStatus": {
        "summary": "Get Task Status",
        "description": "Retrieve the status of a task",
        "value": {"task_id": "task-uuid-here"},
    },
    "CancelTask": {
        "summary": "Cancel Task",
        "description": "Cancel a running task",
        "value": {"task_id": "task-uuid-here"},
    },
}

# Batch Response Examples
BATCH_RESPONSE_EXAMPLES: Dict[str, Dict[str, Any]] = {
    "SuccessResponse": {
        "summary": "Batch Success Response",
        "description": "Response for a successful batch execution",
        "value": {"batch_id": "batch-uuid-here", "status": "pending"},
    }
}

# Run Response Examples
RUN_RESPONSE_EXAMPLES: Dict[str, Dict[str, Any]] = {
    "SuccessResponse": {
        "summary": "Run Success Response",
        "description": "Response for a successful function execution request",
        "value": {"task_id": "task-uuid-here", "status": "pending"},
    }
}

# Pipeline Execution Response Examples
PIPELINE_EXECUTION_RESPONSE_EXAMPLES: Dict[str, Dict[str, Any]] = {
    "SuccessResponse": {
        "summary": "Pipeline Execution Success Response",
        "description": "Response for a successful pipeline execution request",
        "value": {"execution_id": "execution-uuid-here", "status": "pending"},
    }
}

# App Spec Examples
APP_SPEC_EXAMPLES: Dict[str, Dict[str, Any]] = {
    "BasicAppSpec": {
        "summary": "Basic App Specification",
        "description": "Example application specification",
        "value": {
            "name": "PyGUIzer App",
            "description": "Generated by PyGUIzer",
            "functions": [
                {
                    "name": "add",
                    "display_name": "add",
                    "description": "Add two numbers",
                    "layout": {},
                    "group": "default",
                },
                {
                    "name": "multiply",
                    "display_name": "multiply",
                    "description": "Multiply two numbers",
                    "layout": {},
                    "group": "default",
                },
            ],
        },
    }
}

# All examples combined
ALL_EXAMPLES: Dict[str, Dict[str, Any]] = {
    "run": RUN_EXAMPLES,
    "batch": BATCH_EXAMPLES,
    "presets": PRESET_EXAMPLES,
    "pipelines": PIPELINE_EXAMPLES,
    "pipeline_nodes": PIPELINE_NODE_EXAMPLES,
    "pipeline_connections": PIPELINE_CONNECTION_EXAMPLES,
    "pipeline_execution": PIPELINE_EXECUTION_EXAMPLES,
    "tasks": TASK_EXAMPLES,
    "batch_response": BATCH_RESPONSE_EXAMPLES,
    "run_response": RUN_RESPONSE_EXAMPLES,
    "pipeline_execution_response": PIPELINE_EXECUTION_RESPONSE_EXAMPLES,
    "app_spec": APP_SPEC_EXAMPLES,
}

# Test data for common functions
TEST_FUNCTIONS = {
    "add": {
        "description": "Add two numbers",
        "parameters": [
            {
                "name": "a",
                "type": "int",
                "default": None,
                "description": "First number",
            },
            {
                "name": "b",
                "type": "int",
                "default": None,
                "description": "Second number",
            },
        ],
        "return_type": "int",
    },
    "multiply": {
        "description": "Multiply two numbers",
        "parameters": [
            {
                "name": "x",
                "type": "int",
                "default": None,
                "description": "First number",
            },
            {
                "name": "y",
                "type": "int",
                "default": None,
                "description": "Second number",
            },
        ],
        "return_type": "int",
    },
    "async_add": {
        "description": "Async add two numbers",
        "parameters": [
            {
                "name": "a",
                "type": "int",
                "default": None,
                "description": "First number",
            },
            {
                "name": "b",
                "type": "int",
                "default": None,
                "description": "Second number",
            },
        ],
        "return_type": "int",
    },
    "async_multiply": {
        "description": "Async multiply two numbers",
        "parameters": [
            {
                "name": "x",
                "type": "int",
                "default": None,
                "description": "First number",
            },
            {
                "name": "y",
                "type": "int",
                "default": None,
                "description": "Second number",
            },
        ],
        "return_type": "int",
    },
}
