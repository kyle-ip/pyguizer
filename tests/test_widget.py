"""Unit tests for widget specification object (WSO) generation functionality."""

import pytest
from pyguizer.core.widget import generate_wso, WidgetType


@pytest.fixture
def sample_parameters():
    """Fixture providing sample parameters for testing."""
    return [
        {
            "name": "name",
            "type": str,
            "default": None,
            "required": True,
            "kind": "POSITIONAL_OR_KEYWORD"
        },
        {
            "name": "age",
            "type": int,
            "default": 30,
            "required": False,
            "kind": "POSITIONAL_OR_KEYWORD"
        },
        {
            "name": "is_active",
            "type": bool,
            "default": True,
            "required": False,
            "kind": "POSITIONAL_OR_KEYWORD"
        },
        {
            "name": "score",
            "type": float,
            "default": 0.0,
            "required": False,
            "kind": "POSITIONAL_OR_KEYWORD"
        }
    ]

def test_generate_wso_basic(sample_parameters):
    """Test basic WSO generation from parameters."""
    wsos = generate_wso(sample_parameters)
    
    assert len(wsos) == 4
    
    # Verify each WSO has required fields
    for wso in wsos:
        assert "id" in wso
        assert "label" in wso
        assert "type" in wso
        assert "default" in wso
        assert "required" in wso
        assert "data_type" in wso
        assert "constraints" in wso

def test_generate_wso_text_widget(sample_parameters):
    """Test that string type generates text widget."""
    wsos = generate_wso(sample_parameters)
    name_wso = next(wso for wso in wsos if wso["id"] == "name")
    
    assert name_wso["type"] == WidgetType.TEXT
    assert name_wso["label"] == "Name"
    assert name_wso["required"] is True
    assert name_wso["default"] is None

def test_generate_wso_number_widget(sample_parameters):
    """Test that int type generates number widget."""
    wsos = generate_wso(sample_parameters)
    age_wso = next(wso for wso in wsos if wso["id"] == "age")
    
    assert age_wso["type"] == WidgetType.NUMBER
    assert age_wso["label"] == "Age"
    assert age_wso["required"] is False
    assert age_wso["default"] == 30
    assert age_wso["constraints"]["integer"] is True

def test_generate_wso_boolean_widget(sample_parameters):
    """Test that bool type generates boolean widget."""
    wsos = generate_wso(sample_parameters)
    active_wso = next(wso for wso in wsos if wso["id"] == "is_active")
    
    assert active_wso["type"] == WidgetType.BOOLEAN
    assert active_wso["label"] == "Is Active"
    assert active_wso["required"] is False
    assert active_wso["default"] is True

def test_generate_wso_slider_widget(sample_parameters):
    """Test that float type generates slider widget."""
    wsos = generate_wso(sample_parameters)
    score_wso = next(wso for wso in wsos if wso["id"] == "score")
    
    assert score_wso["type"] == WidgetType.SLIDER
    assert score_wso["label"] == "Score"
    assert score_wso["required"] is False
    assert score_wso["default"] == 0.0
    assert "min" in score_wso["constraints"]
    assert "max" in score_wso["constraints"]
    assert "step" in score_wso["constraints"]