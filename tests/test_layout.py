"""Unit tests for layout processing functionality."""

import pytest
from pyguizer.core.layout import process_layout


@pytest.fixture
def sample_wsos():
    """Fixture providing sample Widget Specification Objects."""
    return [
        {
            "id": "name",
            "type": "text",
            "label": "Name",
            "default": None,
            "required": True,
            "data_type": "str",
            "constraints": {}
        },
        {
            "id": "age",
            "type": "number",
            "label": "Age",
            "default": 30,
            "required": False,
            "data_type": "int",
            "constraints": {"integer": True}
        },
        {
            "id": "is_active",
            "type": "boolean",
            "label": "Is Active",
            "default": True,
            "required": False,
            "data_type": "bool",
            "constraints": {}
        }
    ]

def test_process_layout_no_config(sample_wsos):
    """Test layout processing with no configuration."""
    layout_config = {}
    result = process_layout(sample_wsos, layout_config)
    
    assert len(result["sections"]) == 1
    assert result["sections"][0]["name"] == "Main"
    assert len(result["sections"][0]["widgets"]) == 3

def test_process_layout_with_sections(sample_wsos):
    """Test layout processing with custom sections."""
    layout_config = {
        "sections": [
            {
                "name": "Personal Info",
                "widgets": ["name", "age"]
            },
            {
                "name": "Status",
                "widgets": ["is_active"]
            }
        ]
    }
    
    result = process_layout(sample_wsos, layout_config)
    
    assert len(result["sections"]) == 2
    assert result["sections"][0]["name"] == "Personal Info"
    assert len(result["sections"][0]["widgets"]) == 2
    assert result["sections"][1]["name"] == "Status"
    assert len(result["sections"][1]["widgets"]) == 1

def test_process_layout_unassigned_widgets(sample_wsos):
    """Test that unassigned widgets are added to the first section."""
    layout_config = {
        "sections": [
            {
                "name": "Main",
                "widgets": ["name"]
            }
        ]
    }
    
    result = process_layout(sample_wsos, layout_config)
    
    assert len(result["sections"]) == 1
    assert len(result["sections"][0]["widgets"]) == 3  # All widgets should be in the first section

def test_process_layout_empty_sections(sample_wsos):
    """Test layout processing with empty sections."""
    layout_config = {
        "sections": [
            {
                "name": "Empty Section",
                "widgets": []
            }
        ]
    }
    
    result = process_layout(sample_wsos, layout_config)
    
    assert len(result["sections"]) == 1
    assert len(result["sections"][0]["widgets"]) == 3  # All widgets should be added to the empty section

def test_process_layout_unknown_widget_id(sample_wsos):
    """Test layout processing with unknown widget IDs."""
    layout_config = {
        "sections": [
            {
                "name": "Main",
                "widgets": ["name", "unknown_widget"]
            }
        ]
    }
    
    result = process_layout(sample_wsos, layout_config)
    
    assert len(result["sections"]) == 1
    # Should only contain the known widget plus unassigned widgets
    # Unknown widget IDs should be ignored
    assert len(result["sections"][0]["widgets"]) == 3