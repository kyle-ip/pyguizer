"""WebSocket connection manager for PyGUIzer"""

from typing import Any, Dict, Set

from fastapi import WebSocket


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
