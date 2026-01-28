"""Pydantic models for PyGUIzer API"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


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


class BatchFunction(BaseModel):
    """Model for a function in a batch request."""

    name: str = Field(..., description="Function name")
    inputs: Dict[str, Any] = Field(default_factory=dict, description="Function inputs")


class BatchRequest(BaseModel):
    """Request model for batch processing."""

    functions: List[BatchFunction] = Field(
        ..., description="List of functions to run in batch"
    )


class BatchResponse(BaseModel):
    """Response model for batch processing."""

    batch_id: str = Field(...)
    status: TaskStatus = Field(...)


class AppSpec(BaseModel):
    """Application specification model."""

    name: str = Field(...)
    description: str = Field(...)
    functions: List[Dict[str, Any]] = Field(...)


class PipelineExecutionMode(str, Enum):
    """Pipeline execution mode enumeration."""

    SERIAL = "serial"
    PARALLEL = "parallel"


class PipelineNode(BaseModel):
    """Pipeline node model."""

    id: str = Field(...)
    function_name: str = Field(...)
    node_name: str = Field(...)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    position: Optional[Dict[str, float]] = Field(None)


class PipelineConnection(BaseModel):
    """Pipeline connection model."""

    id: str = Field(...)
    source_node_id: str = Field(...)
    source_output: str = Field(...)
    target_node_id: str = Field(...)
    target_input: str = Field(...)


class Pipeline(BaseModel):
    """Pipeline model."""

    id: str = Field(...)
    name: str = Field(...)
    description: str = Field(...)
    nodes: List[PipelineNode] = Field(default_factory=list)
    connections: List[PipelineConnection] = Field(default_factory=list)
    created_at: float = Field(...)
    updated_at: float = Field(...)


class PipelineCreate(BaseModel):
    """Request model for creating a pipeline."""

    name: str = Field(...)
    description: str = Field(...)


class PipelineUpdate(BaseModel):
    """Request model for updating a pipeline."""

    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)


class PipelineNodeCreate(BaseModel):
    """Request model for creating a pipeline node."""

    function_name: str = Field(...)
    node_name: str = Field(...)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    position: Optional[Dict[str, float]] = Field(None)


class PipelineNodeUpdate(BaseModel):
    """Request model for updating a pipeline node."""

    node_name: Optional[str] = Field(None)
    parameters: Optional[Dict[str, Any]] = Field(None)
    position: Optional[Dict[str, float]] = Field(None)


class PipelineConnectionCreate(BaseModel):
    """Request model for creating a pipeline connection."""

    source_node_id: str = Field(...)
    source_output: str = Field(...)
    target_node_id: str = Field(...)
    target_input: str = Field(...)


class PipelineExecutionRequest(BaseModel):
    """Request model for pipeline execution."""

    execution_mode: PipelineExecutionMode = Field(default=PipelineExecutionMode.SERIAL)
    run_async: bool = Field(default=True)


class PipelineExecutionResponse(BaseModel):
    """Response model for pipeline execution."""

    execution_id: str = Field(...)
    status: TaskStatus = Field(...)


__all__ = [
    "TaskStatus",
    "RunRequest",
    "RunResponse",
    "TaskInfo",
    "PresetCreate",
    "PresetUpdate",
    "PresetResponse",
    "BatchFunction",
    "BatchRequest",
    "BatchResponse",
    "AppSpec",
    "PipelineExecutionMode",
    "PipelineNode",
    "PipelineConnection",
    "Pipeline",
    "PipelineCreate",
    "PipelineUpdate",
    "PipelineNodeCreate",
    "PipelineNodeUpdate",
    "PipelineConnectionCreate",
    "PipelineExecutionRequest",
    "PipelineExecutionResponse",
]
