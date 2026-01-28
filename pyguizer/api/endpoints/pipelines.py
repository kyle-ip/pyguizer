"""Pipeline-related endpoints for PyGUIzer"""

import time
from typing import List

from fastapi import APIRouter, Body, Depends

from pyguizer.api.dependencies import get_pyguizer_app, get_task_manager
from pyguizer.api.examples import (
    PIPELINE_CONNECTION_EXAMPLES,
    PIPELINE_EXAMPLES,
    PIPELINE_EXECUTION_EXAMPLES,
    PIPELINE_NODE_EXAMPLES,
)
from pyguizer.api.models import (
    Pipeline,
    PipelineConnection,
    PipelineConnectionCreate,
    PipelineCreate,
    PipelineExecutionRequest,
    PipelineExecutionResponse,
    PipelineNode,
    PipelineNodeCreate,
    PipelineNodeUpdate,
    PipelineUpdate,
)

router = APIRouter(prefix="/api/pipelines", tags=["pipelines"])


@router.get("", response_model=List[Pipeline])
async def get_pipelines(pyguizer_app=Depends(get_pyguizer_app)):
    """Get all pipelines."""
    return pyguizer_app.get_pipelines()


@router.post("", response_model=Pipeline)
async def create_pipeline(
    pipeline_data: PipelineCreate = Body(..., openapi_examples=PIPELINE_EXAMPLES),
    pyguizer_app=Depends(get_pyguizer_app),
):
    """Create a new pipeline."""
    return pyguizer_app.create_pipeline(
        name=pipeline_data.name,
        description=pipeline_data.description,
    )


@router.get("/{pipeline_id}", response_model=Pipeline)
async def get_pipeline(pipeline_id: str, pyguizer_app=Depends(get_pyguizer_app)):
    """Get a pipeline by ID."""
    return pyguizer_app.get_pipeline(pipeline_id)


@router.put("/{pipeline_id}", response_model=Pipeline)
async def update_pipeline(
    pipeline_id: str,
    pipeline_data: PipelineUpdate,
    pyguizer_app=Depends(get_pyguizer_app),
):
    """Update a pipeline by ID."""
    return pyguizer_app.update_pipeline(
        pipeline_id=pipeline_id,
        name=pipeline_data.name,
        description=pipeline_data.description,
    )


@router.delete("/{pipeline_id}")
async def delete_pipeline(pipeline_id: str, pyguizer_app=Depends(get_pyguizer_app)):
    """Delete a pipeline by ID."""
    return pyguizer_app.delete_pipeline(pipeline_id)


@router.post("/{pipeline_id}/validate")
async def validate_pipeline(pipeline_id: str, pyguizer_app=Depends(get_pyguizer_app)):
    """Validate a pipeline configuration."""
    return pyguizer_app.validate_pipeline(pipeline_id)


@router.post("/{pipeline_id}/nodes", response_model=PipelineNode)
async def add_pipeline_node(
    pipeline_id: str,
    node_data: PipelineNodeCreate = Body(..., openapi_examples=PIPELINE_NODE_EXAMPLES),
    pyguizer_app=Depends(get_pyguizer_app),
):
    """Add a node to a pipeline."""
    return pyguizer_app.add_node_to_pipeline(pipeline_id, node_data)


@router.put("/{pipeline_id}/nodes/{node_id}", response_model=PipelineNode)
async def update_pipeline_node(
    pipeline_id: str,
    node_id: str,
    node_data: PipelineNodeUpdate,
    pyguizer_app=Depends(get_pyguizer_app),
):
    """Update a pipeline node."""
    return pyguizer_app.update_pipeline_node(pipeline_id, node_id, node_data)


@router.delete("/{pipeline_id}/nodes/{node_id}")
async def delete_pipeline_node(
    pipeline_id: str, node_id: str, pyguizer_app=Depends(get_pyguizer_app)
):
    """Delete a pipeline node."""
    return pyguizer_app.delete_pipeline_node(pipeline_id, node_id)


@router.post("/{pipeline_id}/connections", response_model=PipelineConnection)
async def add_pipeline_connection(
    pipeline_id: str,
    connection_data: PipelineConnectionCreate = Body(
        ..., openapi_examples=PIPELINE_CONNECTION_EXAMPLES
    ),
    pyguizer_app=Depends(get_pyguizer_app),
):
    """Add a connection to a pipeline."""
    return pyguizer_app.add_connection_to_pipeline(pipeline_id, connection_data)


@router.delete("/{pipeline_id}/connections/{connection_id}")
async def delete_pipeline_connection(
    pipeline_id: str, connection_id: str, pyguizer_app=Depends(get_pyguizer_app)
):
    """Delete a pipeline connection."""
    return pyguizer_app.delete_pipeline_connection(pipeline_id, connection_id)


@router.post("/{pipeline_id}/execute", response_model=PipelineExecutionResponse)
async def execute_pipeline(
    pipeline_id: str,
    execution_request: PipelineExecutionRequest = Body(
        ..., openapi_examples=PIPELINE_EXECUTION_EXAMPLES
    ),
    pyguizer_app=Depends(get_pyguizer_app),
    task_manager=Depends(get_task_manager),
):
    """Execute a pipeline."""
    # Create an execution task
    execution_task_id = task_manager.create_task()
    task_manager.update_task(
        execution_task_id,
        status="running",
        started_at=time.time(),
        progress=0.0,
        message=f"Starting pipeline execution: {pipeline_id}",
    )

    # Execute pipeline synchronously for debugging
    import logging

    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Starting pipeline execution for {pipeline_id}")
        result = await pyguizer_app.execute_pipeline(
            pipeline_id=pipeline_id,
            execution_mode=execution_request.execution_mode.value,
            run_async=execution_request.run_async,
        )
        logger.info(
            f"Pipeline execution completed for {pipeline_id}, updating task status"
        )
        task_manager.update_task(
            execution_task_id,
            status="success",
            completed_at=time.time(),
            progress=1.0,
            message="Pipeline execution completed successfully",
            result=result,
        )
    except Exception as e:
        logger.error(f"Pipeline execution failed for {pipeline_id}: {str(e)}")
        task_manager.update_task(
            execution_task_id,
            status="failed",
            completed_at=time.time(),
            error=str(e),
            message="Pipeline execution failed",
        )

    return PipelineExecutionResponse(
        execution_id=execution_task_id,
        status="pending",
    )
