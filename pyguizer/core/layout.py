"""Layout Processing Module"""

from typing import Any, Dict, List, Set


def process_layout(wsos: List[Dict[str, Any]], layout_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process layout configuration and merge with Widget Specification Objects.
    
    Args:
        wsos: List of Widget Specification Objects.
        layout_config: Layout configuration dictionary.
        
    Returns:
        Processed UI Layout Schema.
    """
    # Get all widget ids
    widget_ids = {wso["id"] for wso in wsos}
    
    # Create a set of all widgets mentioned in the layout
    layout_widgets = set()
    
    def collect_widgets(container: Dict[str, Any]):
        """Recursively collect all widgets from containers"""
        if "widgets" in container:
            layout_widgets.update(container["widgets"])
        
        # Process nested containers based on type
        container_type = container.get("type", "section")
        
        if container_type == "tabs":
            for tab in container.get("tabs", []):
                collect_widgets(tab)
        elif container_type == "accordion":
            for item in container.get("items", []):
                collect_widgets(item)
        elif container_type == "section":
            # Sections can have nested containers in "content"
            if "content" in container:
                for nested_container in container.get("content", []):
                    collect_widgets(nested_container)
        elif container_type == "grid":
            # Grid has rows of columns with widgets
            for row in container.get("rows", []):
                for col in row.get("columns", []):
                    collect_widgets(col)
    
    # Start collecting from the root containers
    root_containers = layout_config.get("containers", layout_config.get("sections", [{"name": "Main", "widgets": []}]))
    for container in root_containers:
        collect_widgets(container)
    
    # Find unassigned widgets
    unassigned_widgets = widget_ids - layout_widgets
    
    # Create processed UI Layout Schema
    ui_layout = {
        "containers": []
    }
    
    def process_container(container: Dict[str, Any], level: int = 0, is_first: bool = False) -> Dict[str, Any]:
        """Recursively process containers"""
        processed = container.copy()
        container_type = container.get("type", "section")
        
        # Process widgets for this container
        container_widgets = []
        widgets_to_process = container.get("widgets", [])
        
        # Handle unassigned widgets based on container type
        if is_first and unassigned_widgets:
            if container_type == "section":
                # Add unassigned widgets directly to section
                widgets_to_process = widgets_to_process + list(unassigned_widgets)
            elif container_type in ["tabs", "accordion"]:
                # Add unassigned widgets to the first child container
                if container_type == "tabs" and container.get("tabs"):
                    # We'll add these to the first tab later in the recursive call
                    pass
                elif container_type == "accordion" and container.get("items"):
                    # We'll add these to the first accordion item later
                    pass
            elif container_type == "grid":
                # Add unassigned widgets to the first cell
                if container.get("rows") and container.get("rows")[0].get("columns"):
                    pass
        
        # Find corresponding WSOs for each widget ID
        for widget_id in widgets_to_process:
            wso = next((w for w in wsos if w["id"] == widget_id), None)
            if wso:
                container_widgets.append(wso)
        
        processed["widgets"] = container_widgets
        
        # Process nested containers
        if container_type == "tabs":
            processed_tabs = []
            for i, tab in enumerate(container.get("tabs", [])):
                # Add unassigned widgets to the first tab
                if i == 0 and is_first and unassigned_widgets:
                    tab = tab.copy()
                    tab["widgets"] = tab.get("widgets", []) + list(unassigned_widgets)
                processed_tabs.append(process_container(tab, level + 1))
            processed["tabs"] = processed_tabs
        elif container_type == "accordion":
            processed_items = []
            for i, item in enumerate(container.get("items", [])):
                # Add unassigned widgets to the first accordion item
                if i == 0 and is_first and unassigned_widgets:
                    item = item.copy()
                    item["widgets"] = item.get("widgets", []) + list(unassigned_widgets)
                processed_items.append(process_container(item, level + 1))
            processed["items"] = processed_items
        elif container_type == "section":
            processed["content"] = [process_container(nested, level + 1) for nested in container.get("content", [])]
        elif container_type == "grid":
            processed["rows"] = []
            for row_idx, row in enumerate(container.get("rows", [])):
                processed_row = row.copy()
                processed_row["columns"] = []
                for col_idx, col in enumerate(row.get("columns", [])):
                    # Add unassigned widgets to the first cell
                    if row_idx == 0 and col_idx == 0 and is_first and unassigned_widgets:
                        col = col.copy()
                        col["widgets"] = col.get("widgets", []) + list(unassigned_widgets)
                    processed_row["columns"].append(process_container(col, level + 1))
                processed["rows"].append(processed_row)
        
        return processed
    
    # Process all root containers
    for i, container in enumerate(root_containers):
        processed_container = process_container(container, is_first=(i == 0))
        ui_layout["containers"].append(processed_container)
    
    # For backward compatibility, keep sections key if no containers specified
    if "containers" not in layout_config and "sections" in layout_config:
        ui_layout["sections"] = [container for container in ui_layout["containers"] if container.get("type", "section") == "section"]
    
    return ui_layout
