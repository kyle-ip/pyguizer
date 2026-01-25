"""FastAPI Application for PyGUIzer"""

import asyncio
import time
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional, Set

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from pyguizer.core.introspection import introspect_function
from pyguizer.core.layout import process_layout
from pyguizer.core.widget import generate_wso


class TaskStatus(str, Enum):
    """Task status enumeration."""

    PENDING = "pending"
    RUNNING = "running"
    STREAMING = "streaming"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RunRequest(BaseModel):
    """Request model for running a function."""

    func_name: str = Field(...)
    inputs: Dict[str, Any] = Field(...)


class RunResponse(BaseModel):
    """Response model for function execution."""

    task_id: str = Field(...)
    status: TaskStatus = Field(...)


class TaskInfo(BaseModel):
    """Task information model."""

    task_id: str = Field(...)
    status: TaskStatus = Field(...)
    created_at: float = Field(...)
    started_at: Optional[float] = Field(None)
    completed_at: Optional[float] = Field(None)
    result: Optional[Any] = Field(None)
    error: Optional[str] = Field(None)
    progress: Optional[float] = Field(None)
    message: Optional[str] = Field(None)


class PresetCreate(BaseModel):
    """Request model for creating a preset."""

    name: str = Field(..., description="Preset name")
    description: Optional[str] = Field(None, description="Preset description")
    values: Dict[str, Any] = Field(..., description="Preset values")


class PresetUpdate(BaseModel):
    """Request model for updating a preset."""

    name: Optional[str] = Field(None, description="Preset name")
    description: Optional[str] = Field(None, description="Preset description")
    values: Optional[Dict[str, Any]] = Field(None, description="Preset values")


class PresetResponse(BaseModel):
    """Response model for preset operations."""

    id: str = Field(...)
    name: str = Field(...)
    description: Optional[str] = Field(None)
    values: Dict[str, Any] = Field(...)
    created_at: float = Field(...)
    updated_at: Optional[float] = Field(None)


class AppSpec(BaseModel):
    """Application specification model."""

    name: str = Field(...)
    description: str = Field(...)
    functions: List[Dict[str, Any]] = Field(...)


class ConnectionManager:
    """WebSocket connection manager."""

    def __init__(self):
        # Maps task_id to set of WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, task_id: str):
        """Accept a WebSocket connection for a specific task."""
        await websocket.accept()
        if task_id not in self.active_connections:
            self.active_connections[task_id] = set()
        self.active_connections[task_id].add(websocket)

    def disconnect(self, websocket: WebSocket, task_id: str):
        """Disconnect a WebSocket connection from a specific task."""
        if task_id in self.active_connections:
            self.active_connections[task_id].discard(websocket)
            if not self.active_connections[task_id]:
                del self.active_connections[task_id]

    async def send_personal_message(
        self, message: Dict[str, Any], websocket: WebSocket
    ):
        """Send a message to a specific WebSocket connection."""
        await websocket.send_json(message)

    async def broadcast(self, message: Dict[str, Any], task_id: str):
        """Broadcast a message to all connections for a specific task."""
        if task_id in self.active_connections:
            for connection in self.active_connections[task_id]:
                await connection.send_json(message)


class TaskManager:
    """Task manager for handling asynchronous function execution."""

    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.manager = ConnectionManager()

    def create_task(self) -> str:
        """Create a new task and return its ID."""
        task_id = str(uuid.uuid4())
        self.tasks[task_id] = {
            "status": TaskStatus.PENDING,
            "created_at": time.time(),
            "started_at": None,
            "completed_at": None,
            "result": None,
            "error": None,
            "progress": None,
            "message": None,
            "cancelled": False,
        }
        return task_id

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get task information by ID."""
        if task_id not in self.tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        return self.tasks[task_id]

    def update_task(self, task_id: str, **kwargs):
        """Update task information."""
        task = self.get_task(task_id)
        task.update(kwargs)
        # Broadcast updates to connected WebSockets
        asyncio.create_task(
            self.manager.broadcast(
                {"type": "task_update", "task_id": task_id, "task": task}, task_id
            )
        )

    def cancel_task(self, task_id: str):
        """Cancel a running task."""
        task = self.get_task(task_id)
        task["cancelled"] = True
        task["status"] = TaskStatus.CANCELLED
        task["completed_at"] = time.time()
        task["message"] = "Task cancelled by user"
        # Broadcast cancellation to connected WebSockets
        asyncio.create_task(
            self.manager.broadcast(
                {"type": "task_update", "task_id": task_id, "task": task}, task_id
            )
        )


class PyGUIzerApp:
    """Main PyGUIzer application class."""

    def __init__(self, func=None, layout=None):
        self.layout = layout or {
            "containers": [{"name": "Main", "type": "section", "widgets": []}]
        }

        # Function registry - maps function name to function metadata
        self.function_registry = {}

        # Preset management
        self.presets = []

        # If a function is provided during initialization, register it
        if func:
            self.register_function(func)

    def register_function(self, func, layout=None):
        """Register a new function with the application."""
        # Introspect the function
        func_info = introspect_function(func)

        # Generate WSOs
        wsos = generate_wso(func_info["parameters"])

        # Process layout for this function
        function_layout = process_layout(wsos, layout or self.layout)

        # Register the function
        func_name = func.__name__
        self.function_registry[func_name] = {
            "func": func,
            "func_info": func_info,
            "wsos": wsos,
            "ui_layout": function_layout,
        }

    def get_app_spec(self) -> Dict[str, Any]:
        """Get the application specification."""
        # Build function specs for all registered functions
        functions = []
        for func_name, func_data in self.function_registry.items():
            functions.append(
                {
                    "name": func_name,
                    "display_name": func_data["func_info"]["name"],
                    "description": func_data["func_info"]["docstring"],
                    "layout": func_data["ui_layout"],
                }
            )

        return {
            "name": "PyGUIzer App",
            "description": "Multi-function PyGUIzer Application",
            "functions": functions,
        }

    def run_function(self, func_name: str, inputs: Dict[str, Any]) -> Any:
        """Run a registered function with provided inputs."""
        if func_name not in self.function_registry:
            raise HTTPException(
                status_code=404, detail=f"Function '{func_name}' not found"
            )

        func = self.function_registry[func_name]["func"]
        try:
            return func(**inputs)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_presets(self) -> List[Dict[str, Any]]:
        """Get all presets."""
        return self.presets

    def create_preset(
        self, name: str, description: str, values: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new preset."""
        preset = {
            "id": str(uuid.uuid4()),
            "name": name,
            "description": description,
            "values": values,
            "created_at": time.time(),
        }
        self.presets.append(preset)
        return preset

    def get_preset(self, preset_id: str) -> Dict[str, Any]:
        """Get a preset by ID."""
        for preset in self.presets:
            if preset["id"] == preset_id:
                return preset
        raise HTTPException(status_code=404, detail="Preset not found")

    def update_preset(
        self,
        preset_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        values: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Update a preset by ID."""
        preset = self.get_preset(preset_id)
        if name is not None:
            preset["name"] = name
        if description is not None:
            preset["description"] = description
        if values is not None:
            preset["values"] = values
        preset["updated_at"] = time.time()
        return preset

    def delete_preset(self, preset_id: str) -> Dict[str, Any]:
        """Delete a preset by ID."""
        preset = self.get_preset(preset_id)
        self.presets.remove(preset)
        return {
            "status": "deleted",
            "message": f"Preset {preset_id} deleted successfully",
        }


async def execute_task(
    pyguizer_app: PyGUIzerApp,
    task_manager: TaskManager,
    task_id: str,
    func_name: str,
    inputs: Dict[str, Any],
):
    """Execute a task asynchronously with progress updates."""
    try:
        # Update task status to running
        task_manager.update_task(
            task_id,
            status=TaskStatus.RUNNING,
            started_at=time.time(),
            progress=0.0,
            message="Task started",
        )

        # Simulate progress updates
        for i in range(0, 100, 20):
            task_manager.update_task(
                task_id, progress=i / 100, message=f"Processing... {i}%"
            )
            await asyncio.sleep(0)

            # Check if task was cancelled
            task = task_manager.get_task(task_id)
            if task["cancelled"]:
                return

        # Run the actual function
        result = pyguizer_app.run_function(func_name, inputs)

        # Update task status to success
        task_manager.update_task(
            task_id,
            status=TaskStatus.SUCCESS,
            completed_at=time.time(),
            progress=1.0,
            message="Task completed successfully",
            result=result,
        )

    except Exception as e:
        # Update task status to failed
        task_manager.update_task(
            task_id,
            status=TaskStatus.FAILED,
            completed_at=time.time(),
            error=str(e),
            message="Task failed",
        )


def create_app(pyguizer_app=None, func=None, layout=None):
    """Create a FastAPI app for the given function(s)."""
    app = FastAPI(title="PyGUIzer App", description="Generated by PyGUIzer")
    # Use provided pyguizer_app instance or create a new one
    # If pyguizer_app is a function (not a PyGUIzerApp instance), treat it as func
    if pyguizer_app is not None and not isinstance(pyguizer_app, PyGUIzerApp) and callable(pyguizer_app):
        # First positional arg is a function, shift parameters
        if func is None:
            # create_app(func) -> func is in pyguizer_app position
            func = pyguizer_app
            pyguizer_app = None
        elif layout is None:
            # create_app(func, layout) -> func is in pyguizer_app, layout is in func
            actual_func = pyguizer_app
            actual_layout = func
            func = actual_func
            layout = actual_layout
            pyguizer_app = None
    
    if pyguizer_app is None:
        pyguizer_app = PyGUIzerApp(func, layout)
    task_manager = TaskManager()

    # Define API routes first (order matters!)
    @app.get("/api/spec")
    async def get_spec():
        """Get the application specification."""
        return pyguizer_app.get_app_spec()

    @app.post("/api/run", response_model=RunResponse)
    async def run(request: RunRequest):
        """Run a function with provided inputs."""
        # Create a new task
        task_id = task_manager.create_task()

        # Start task execution in the background
        asyncio.create_task(
            execute_task(
                pyguizer_app, task_manager, task_id, request.func_name, request.inputs
            )
        )

        return RunResponse(task_id=task_id, status=TaskStatus.PENDING)

    @app.get("/api/functions")
    async def get_functions():
        """Get all registered functions."""
        return [
            {
                "name": func_name,
                "display_name": func_data["func_info"]["name"],
                "description": func_data["func_info"]["docstring"],
            }
            for func_name, func_data in pyguizer_app.function_registry.items()
        ]

    @app.get("/api/functions/{func_name}")
    async def get_function(func_name: str):
        """Get details for a specific function."""
        try:
            if func_name not in pyguizer_app.function_registry:
                raise HTTPException(
                    status_code=404, detail=f"Function '{func_name}' not found"
                )

            func_data = pyguizer_app.function_registry[func_name]

            # Convert parameter types to strings for JSON serialization
            parameters = []
            for param in func_data["func_info"]["parameters"]:
                param_copy = param.copy()
                param_type = param_copy["type"]
                # Handle different type representations
                if hasattr(param_type, "__name__"):
                    param_copy["type"] = param_type.__name__
                elif hasattr(param_type, "_name"):
                    param_copy["type"] = param_type._name
                else:
                    param_copy["type"] = str(param_type)
                parameters.append(param_copy)

            # Check if layout is serializable
            layout = func_data["ui_layout"]

            # Determine output information
            return_type = func_data["func_info"]["return_type"]
            outputs = []

            # If return type is a dict or tuple, we can extract multiple outputs
            # For now, we'll always include "result" as the default output
            # and add additional outputs if the return type suggests multiple values
            outputs.append(
                {
                    "name": "result",
                    "type": (
                        str(return_type)
                        if hasattr(return_type, "__name__")
                        else str(return_type)
                    ),
                    "description": "Function return value",
                }
            )

            # Check if return type is a tuple or dict to suggest multiple outputs
            if hasattr(return_type, "__origin__"):
                origin = return_type.__origin__
                if origin is dict:
                    # For dict returns, we could extract keys, but that
                    # requires runtime info
                    # For now, just use "result"
                    pass
                elif origin is tuple:
                    # For tuple returns, we could suggest indexed outputs
                    # But we'll keep it simple and just use "result" for now
                    pass

            return {
                "name": func_name,
                "display_name": func_data["func_info"]["name"],
                "description": func_data["func_info"]["docstring"],
                "parameters": parameters,
                "outputs": outputs,
                "layout": layout,
            }
        except Exception as e:
            # Log the detailed error for debugging
            import traceback

            print(f"Error in get_function for {func_name}: {e}")
            print(traceback.format_exc())
            raise HTTPException(
                status_code=500, detail=f"Internal server error: {str(e)}"
            )

    @app.get("/api/tasks/{task_id}", response_model=TaskInfo)
    async def get_task(task_id: str):
        """Get task information by ID."""
        task = task_manager.get_task(task_id)
        return TaskInfo(
            task_id=task_id,
            status=task["status"],
            created_at=task["created_at"],
            started_at=task["started_at"],
            completed_at=task["completed_at"],
            result=task["result"],
            error=task["error"],
            progress=task["progress"],
            message=task["message"],
        )

    @app.post("/api/tasks/{task_id}/cancel")
    async def cancel_task(task_id: str):
        """Cancel a running task."""
        task_manager.cancel_task(task_id)
        return {"status": "cancelled"}

    @app.websocket("/api/tasks/{task_id}/stream")
    async def websocket_endpoint(websocket: WebSocket, task_id: str):
        """WebSocket endpoint for real-time task updates."""
        # Check if task exists
        task_manager.get_task(task_id)

        # Connect WebSocket
        await task_manager.manager.connect(websocket, task_id)

        try:
            # Send initial task status
            task = task_manager.get_task(task_id)
            await websocket.send_json(
                {"type": "task_update", "task_id": task_id, "task": task}
            )

            # Keep connection alive and listen for messages
            while True:
                data = await websocket.receive_json()
                if data.get("type") == "cancel":
                    task_manager.cancel_task(task_id)
        except WebSocketDisconnect:
            task_manager.manager.disconnect(websocket, task_id)

    # Preset management endpoints
    @app.get("/api/presets", response_model=List[PresetResponse])
    async def get_presets():
        """Get all presets."""
        return pyguizer_app.get_presets()

    @app.post("/api/presets", response_model=PresetResponse)
    async def create_preset(preset_data: PresetCreate):
        """Create a new preset."""
        return pyguizer_app.create_preset(
            name=preset_data.name,
            description=preset_data.description,
            values=preset_data.values,
        )

    @app.get("/api/presets/{preset_id}", response_model=PresetResponse)
    async def get_preset(preset_id: str):
        """Get a preset by ID."""
        return pyguizer_app.get_preset(preset_id)

    @app.put("/api/presets/{preset_id}", response_model=PresetResponse)
    async def update_preset(preset_id: str, preset_data: PresetUpdate):
        """Update a preset by ID."""
        return pyguizer_app.update_preset(
            preset_id=preset_id,
            name=preset_data.name,
            description=preset_data.description,
            values=preset_data.values,
        )

    @app.delete("/api/presets/{preset_id}")
    async def delete_preset(preset_id: str):
        """Delete a preset by ID."""
        return pyguizer_app.delete_preset(preset_id)

    # Mount static files for frontend - should come after API routes
    # This way, API requests are routed to the API endpoints, not the static files
    app.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")

    return app
