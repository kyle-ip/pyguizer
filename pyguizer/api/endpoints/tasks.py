"""Task-related endpoints for PyGUIzer"""

import json

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from pyguizer.api.dependencies import get_task_manager

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get(
    "/{task_id}",
    openapi_extra={
        "examples": {
            "GetTaskStatus": {
                "summary": "Get Task Status",
                "description": "Retrieve the status of a task",
                "value": {"task_id": "task-uuid-here"},
            }
        }
    },
)
async def get_task(task_id: str, task_manager=Depends(get_task_manager)):
    """Get task information by ID."""
    import logging

    logger = logging.getLogger(__name__)
    try:
        task = task_manager.get_task(task_id)
        # Create a copy of the task to avoid modifying the original
        task_copy = task.copy()
        # Properly serialize the result to handle circular references
        if task_copy.get("result") is not None:
            try:
                # Serialize the result to JSON and back to break circular references
                task_copy["result"] = json.loads(
                    json.dumps(task_copy["result"], default=str)
                )
            except Exception as e:
                logger.error(f"Error serializing result: {str(e)}", exc_info=True)
                task_copy["result"] = str(task_copy["result"])
        return task_copy
    except Exception as e:
        logger.error(f"Error getting task: {str(e)}", exc_info=True)
        raise


@router.post(
    "/{task_id}/cancel",
    openapi_extra={
        "examples": {
            "CancelTask": {
                "summary": "Cancel Task",
                "description": "Cancel a running task",
                "value": {"task_id": "task-uuid-here"},
            }
        }
    },
)
async def cancel_task(task_id: str, task_manager=Depends(get_task_manager)):
    """Cancel a running task."""
    task_manager.cancel_task(task_id)
    return {"status": "cancelled"}


@router.websocket("/{task_id}/stream")
async def websocket_endpoint(
    websocket: WebSocket, task_id: str, task_manager=Depends(get_task_manager)
):
    """WebSocket endpoint for real-time task updates.

    Example usage:
    1. Connect to ws://localhost:8000/api/tasks/{task_id}/stream
    2. Receive initial task status
    3. Send {"type": "cancel"} to cancel the task
    """

    # Check if task exists
    task_manager.get_task(task_id)

    # Connect WebSocket
    await task_manager.manager.connect(websocket, task_id)

    try:
        # Send initial task status with proper serialization
        task = task_manager.get_task(task_id)
        # Create a safe copy of the task for sending over WebSocket
        task_copy = task.copy()
        # Ensure proper JSON serialization (same as update_task method)
        if task_copy.get("result") is not None:
            try:
                task_copy["result"] = json.loads(
                    json.dumps(task_copy["result"], default=str)
                )
            except Exception:
                task_copy["result"] = str(task_copy["result"])
        # Convert enum values to strings explicitly for consistent serialization
        if isinstance(task_copy.get("status"), str):
            pass  # Already a string
        elif hasattr(task_copy.get("status"), "value"):
            task_copy["status"] = task_copy["status"].value
        await websocket.send_json(
            {"type": "task_update", "task_id": task_id, "task": task_copy}
        )

        # Keep connection alive and listen for messages
        while True:
            data = await websocket.receive_json()
            if data.get("type") == "cancel":
                task_manager.cancel_task(task_id)
    except WebSocketDisconnect:
        task_manager.manager.disconnect(websocket, task_id)
