"""Task manager for PyGUIzer"""

import asyncio
import json
import time
import uuid
from enum import Enum
from typing import Any, Dict

from fastapi import HTTPException

from pyguizer.api.services.connection_manager import ConnectionManager


class TaskManager:
    """Task manager for handling asynchronous function execution."""

    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.manager = ConnectionManager()

    def create_task(self) -> str:
        """Create a new task and return its ID."""
        task_id = str(uuid.uuid4())
        self.tasks[task_id] = {
            "status": "pending",
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
        task = self.tasks[task_id].copy()
        task["task_id"] = task_id
        return task

    def update_task(self, task_id: str, **kwargs):
        """Update task information."""
        if task_id not in self.tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        task = self.tasks[task_id]
        task.update(kwargs)
        # Create a safe copy of the task for broadcasting (serialize result
        # to break circular references)
        task_copy = task.copy()
        task_copy["task_id"] = task_id
        if task_copy.get("result") is not None:
            try:
                # Serialize the result to JSON and back to break circular references
                task_copy["result"] = json.loads(
                    json.dumps(task_copy["result"], default=str)
                )
            except Exception:
                # Fallback to string conversion if serialization fails
                task_copy["result"] = str(task_copy["result"])
        # Convert enum values to strings explicitly for consistent serialization
        if isinstance(task_copy.get("status"), Enum):
            task_copy["status"] = task_copy["status"].value
        # Broadcast updates to connected WebSockets with safe task copy
        asyncio.create_task(
            self.manager.broadcast(
                {"type": "task_update", "task_id": task_id, "task": task_copy}, task_id
            )
        )

    def cancel_task(self, task_id: str):
        """Cancel a running task."""
        if task_id not in self.tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        task = self.tasks[task_id]
        task["cancelled"] = True
        task["status"] = "cancelled"
        task["completed_at"] = time.time()
        task["message"] = "Task cancelled by user"
        # Create a safe copy of the task for broadcasting
        task_copy = task.copy()
        task_copy["task_id"] = task_id
        # Convert enum values to strings explicitly for consistent serialization
        if isinstance(task_copy.get("status"), Enum):
            task_copy["status"] = task_copy["status"].value
        # Broadcast cancellation to connected WebSockets with safe task copy
        asyncio.create_task(
            self.manager.broadcast(
                {"type": "task_update", "task_id": task_id, "task": task_copy}, task_id
            )
        )
