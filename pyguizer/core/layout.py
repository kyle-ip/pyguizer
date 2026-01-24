"""Layout Processing Module"""

from typing import Any, Dict, List


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
    sections = layout_config.get("sections", [{"name": "Main", "widgets": []}])
    
    for section in sections:
        if "widgets" in section:
            layout_widgets.update(section["widgets"])
    
    # Find unassigned widgets
    unassigned_widgets = widget_ids - layout_widgets
    
    # Build the UI Layout Schema without modifying the original config
    ui_layout = {
        "sections": []
    }
    
    # Process each section
    for i, section in enumerate(sections):
        section_widgets = []
        widgets_to_process = section.get("widgets", [])
        
        # Add unassigned widgets to the first section
        if i == 0 and unassigned_widgets:
            widgets_to_process = widgets_to_process + list(unassigned_widgets)
        
        # Find corresponding WSOs for each widget ID
        for widget_id in widgets_to_process:
            wso = next((w for w in wsos if w["id"] == widget_id), None)
            if wso:
                section_widgets.append(wso)
        
        ui_layout["sections"].append({
            "name": section["name"],
            "widgets": section_widgets
        })
    
    return ui_layout
