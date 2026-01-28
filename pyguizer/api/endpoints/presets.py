"""Preset-related endpoints for PyGUIzer"""

from typing import List

from fastapi import APIRouter, Body, Depends

from pyguizer.api.dependencies import get_pyguizer_app
from pyguizer.api.examples import PRESET_EXAMPLES
from pyguizer.api.models import PresetCreate, PresetResponse, PresetUpdate

router = APIRouter(prefix="/api/presets", tags=["presets"])


@router.get("", response_model=List[PresetResponse])
async def get_presets(pyguizer_app=Depends(get_pyguizer_app)):
    """Get all presets."""
    return pyguizer_app.get_presets()


@router.post("", response_model=PresetResponse)
async def create_preset(
    preset_data: PresetCreate = Body(..., openapi_examples=PRESET_EXAMPLES),
    pyguizer_app=Depends(get_pyguizer_app),
):
    """Create a new preset."""
    return pyguizer_app.create_preset(
        name=preset_data.name,
        description=preset_data.description,
        values=preset_data.values,
    )


@router.get("/{preset_id}", response_model=PresetResponse)
async def get_preset(preset_id: str, pyguizer_app=Depends(get_pyguizer_app)):
    """Get a preset by ID."""
    return pyguizer_app.get_preset(preset_id)


@router.put("/{preset_id}", response_model=PresetResponse)
async def update_preset(
    preset_id: str, preset_data: PresetUpdate, pyguizer_app=Depends(get_pyguizer_app)
):
    """Update a preset by ID."""
    return pyguizer_app.update_preset(
        preset_id=preset_id,
        name=preset_data.name,
        description=preset_data.description,
        values=preset_data.values,
    )


@router.delete("/{preset_id}")
async def delete_preset(preset_id: str, pyguizer_app=Depends(get_pyguizer_app)):
    """Delete a preset by ID."""
    return pyguizer_app.delete_preset(preset_id)
