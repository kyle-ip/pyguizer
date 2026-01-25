"""Comprehensive unit tests for the layout module."""



from pyguizer.core.layout import process_layout


class TestLayoutBasic:
    """Test basic layout processing."""

    def test_simple_section_layout(self):
        """Test processing a simple section layout."""
        wsos = [
            {"id": "name", "label": "Name", "type": "text", "required": True},
            {"id": "age", "label": "Age", "type": "number", "required": True},
        ]
        layout_config = {"sections": [{"name": "Main", "widgets": ["name", "age"]}]}

        result = process_layout(wsos, layout_config)

        assert "containers" in result
        assert len(result["containers"]) == 1
        assert len(result["containers"][0]["widgets"]) == 2
        assert result["containers"][0]["widgets"][0]["id"] == "name"
        assert result["containers"][0]["widgets"][1]["id"] == "age"

    def test_containers_layout(self):
        """Test processing containers layout."""
        wsos = [
            {"id": "name", "label": "Name", "type": "text", "required": True},
            {"id": "email", "label": "Email", "type": "text", "required": True},
        ]
        layout_config = {
            "containers": [
                {
                    "name": "Personal Info",
                    "type": "section",
                    "widgets": ["name", "email"],
                }
            ]
        }

        result = process_layout(wsos, layout_config)

        assert "containers" in result
        assert len(result["containers"]) == 1
        assert result["containers"][0]["name"] == "Personal Info"

    def test_unassigned_widgets(self):
        """Test that unassigned widgets are added to first section."""
        wsos = [
            {"id": "name", "label": "Name", "type": "text", "required": True},
            {"id": "age", "label": "Age", "type": "number", "required": True},
            {"id": "email", "label": "Email", "type": "text", "required": True},
        ]
        layout_config = {"sections": [{"name": "Main", "widgets": ["name"]}]}

        result = process_layout(wsos, layout_config)

        # age and email should be added to the first section
        widget_ids = [w["id"] for w in result["containers"][0]["widgets"]]
        assert "name" in widget_ids
        assert "age" in widget_ids or "email" in widget_ids


class TestLayoutTabs:
    """Test tabs container layout."""

    def test_tabs_layout(self):
        """Test processing tabs layout."""
        wsos = [
            {"id": "name", "label": "Name", "type": "text", "required": True},
            {"id": "email", "label": "Email", "type": "text", "required": True},
        ]
        layout_config = {
            "containers": [
                {
                    "type": "tabs",
                    "tabs": [
                        {"name": "Tab 1", "widgets": ["name"]},
                        {"name": "Tab 2", "widgets": ["email"]},
                    ],
                }
            ]
        }

        result = process_layout(wsos, layout_config)

        assert len(result["containers"]) == 1
        assert result["containers"][0]["type"] == "tabs"
        assert len(result["containers"][0]["tabs"]) == 2
        assert len(result["containers"][0]["tabs"][0]["widgets"]) == 1
        assert result["containers"][0]["tabs"][0]["widgets"][0]["id"] == "name"

    def test_tabs_with_unassigned_widgets(self):
        """Test that unassigned widgets go to first tab."""
        wsos = [
            {"id": "name", "label": "Name", "type": "text", "required": True},
            {"id": "age", "label": "Age", "type": "number", "required": True},
        ]
        layout_config = {
            "containers": [
                {"type": "tabs", "tabs": [{"name": "Tab 1", "widgets": ["name"]}]}
            ]
        }

        result = process_layout(wsos, layout_config)

        # age should be added to first tab
        first_tab_widgets = [
            w["id"] for w in result["containers"][0]["tabs"][0]["widgets"]
        ]
        assert "name" in first_tab_widgets
        assert "age" in first_tab_widgets


class TestLayoutAccordion:
    """Test accordion container layout."""

    def test_accordion_layout(self):
        """Test processing accordion layout."""
        wsos = [
            {"id": "name", "label": "Name", "type": "text", "required": True},
            {"id": "email", "label": "Email", "type": "text", "required": True},
        ]
        layout_config = {
            "containers": [
                {
                    "type": "accordion",
                    "items": [
                        {"name": "Item 1", "widgets": ["name"]},
                        {"name": "Item 2", "widgets": ["email"]},
                    ],
                }
            ]
        }

        result = process_layout(wsos, layout_config)

        assert len(result["containers"]) == 1
        assert result["containers"][0]["type"] == "accordion"
        assert len(result["containers"][0]["items"]) == 2


class TestLayoutGrid:
    """Test grid container layout."""

    def test_grid_layout(self):
        """Test processing grid layout."""
        wsos = [
            {"id": "name", "label": "Name", "type": "text", "required": True},
            {"id": "age", "label": "Age", "type": "number", "required": True},
        ]
        layout_config = {
            "containers": [
                {
                    "type": "grid",
                    "rows": [
                        {"columns": [{"widgets": ["name"]}, {"widgets": ["age"]}]}
                    ],
                }
            ]
        }

        result = process_layout(wsos, layout_config)

        assert len(result["containers"]) == 1
        assert result["containers"][0]["type"] == "grid"
        assert len(result["containers"][0]["rows"]) == 1
        assert len(result["containers"][0]["rows"][0]["columns"]) == 2


class TestLayoutNested:
    """Test nested container layouts."""

    def test_nested_sections(self):
        """Test nested sections."""
        wsos = [
            {"id": "name", "label": "Name", "type": "text", "required": True},
            {"id": "age", "label": "Age", "type": "number", "required": True},
        ]
        layout_config = {
            "containers": [
                {
                    "name": "Outer",
                    "type": "section",
                    "widgets": ["name"],
                    "content": [
                        {"name": "Inner", "type": "section", "widgets": ["age"]}
                    ],
                }
            ]
        }

        result = process_layout(wsos, layout_config)

        assert len(result["containers"]) == 1
        assert len(result["containers"][0]["content"]) == 1
        assert result["containers"][0]["content"][0]["widgets"][0]["id"] == "age"


class TestLayoutEdgeCases:
    """Test edge cases in layout processing."""

    def test_empty_widgets(self):
        """Test layout with empty widgets list."""
        wsos = []
        layout_config = {"sections": [{"name": "Main", "widgets": []}]}

        result = process_layout(wsos, layout_config)

        assert len(result["containers"]) == 1
        assert len(result["containers"][0]["widgets"]) == 0

    def test_missing_widget_in_layout(self):
        """Test layout referencing non-existent widget."""
        wsos = [{"id": "name", "label": "Name", "type": "text", "required": True}]
        layout_config = {
            "sections": [{"name": "Main", "widgets": ["name", "nonexistent"]}]
        }

        result = process_layout(wsos, layout_config)

        # Only existing widget should be included
        widget_ids = [w["id"] for w in result["containers"][0]["widgets"]]
        assert "name" in widget_ids
        assert "nonexistent" not in widget_ids

    def test_empty_layout_config(self):
        """Test processing with empty layout config."""
        wsos = [{"id": "name", "label": "Name", "type": "text", "required": True}]
        layout_config = {}

        result = process_layout(wsos, layout_config)

        # Should create default section
        assert "containers" in result
        assert len(result["containers"]) > 0

    def test_backward_compatibility_sections(self):
        """Test backward compatibility with sections key."""
        wsos = [{"id": "name", "label": "Name", "type": "text", "required": True}]
        layout_config = {"sections": [{"name": "Main", "widgets": ["name"]}]}

        result = process_layout(wsos, layout_config)

        # Should have both containers and sections for backward compatibility
        assert "containers" in result
        if "sections" in layout_config:
            assert "sections" in result
