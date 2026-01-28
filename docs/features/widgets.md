# Widget Types

PyGUIzer automatically maps Python types to appropriate UI widgets, providing a seamless experience for both developers and users. This document details the type-to-widget mappings and their capabilities.

## Basic Types

| Python Type | Widget Type | Example | Features |
|------------|-------------|---------|----------|
| `str` | Text Input | `name: str` | Simple text input with placeholder |
| `int` | Number Input | `age: int` | Integer-only input with min/max support |
| `float` | Slider | `temperature: float` | Interactive slider with visual feedback |
| `bool` | Checkbox | `is_active: bool` | Toggle switch with clear state indication |

## Complex Types

| Python Type | Widget Type | Example | Features |
|------------|-------------|---------|----------|
| `List[str]` | Multi-select | `hobbies: List[str]` | Multi-selection dropdown for string lists |
| `Set[str]` | Multi-select | `tags: Set[str]` | Similar to List but enforces uniqueness |
| `Dict` | JSON Editor | `config: Dict[str, Any]` | Full-featured JSON editor for complex data |
| `Tuple` | JSON Editor | `dimensions: Tuple[int, int]` | Structured JSON editing for fixed-size collections |
| `FrozenSet` | Multi-select | `unique_values: FrozenSet[str]` | Immutable set with multi-select interface |
| `Any` | Text Input | `dynamic: Any` | Flexible input for dynamic types |

## Specialized Types

| Python Type | Widget Type | Example | Features |
|------------|-------------|---------|----------|
| `UUID` | Text Input | `user_id: UUID` | Validated input with UUID format checking |
| `Decimal` | Number Input | `price: Decimal` | High-precision decimal input |
| `Path` | File Upload | `file: Path` | File selection widget with upload capabilities |
| `Enum` | Select | `color: Color` | Dropdown with auto-generated enum options |

## DateTime Types

| Python Type | Widget Type | Example | Features |
|------------|-------------|---------|----------|
| `date` | Date Picker | `birth_date: date` | Calendar widget for date selection |
| `time` | Time Picker | `meeting_time: time` | Time selection widget with format support |
| `datetime` | DateTime Picker | `event: datetime` | Combined date and time selection |

## Custom Types

| Python Type | Widget Type | Example | Features |
|------------|-------------|---------|----------|
| Dataclass | JSON Editor | `user: User` | Smart handling of dataclass structures |
| Third-party | Auto-mapped | `third_party: LibraryClass` | Inheritance-based mapping for external classes |

## Advanced Widget Features

### File Upload Widget

The file upload widget supports:
- Drag-and-drop functionality
- Progress tracking for large files
- File type validation
- Multiple file selection (for `List[Path]`)

### Color Picker Widget

The color picker widget provides:
- Visual color selection
- Hex color code input
- Color preview
- Support for both background and text colors

### Date/Time Pickers

Date and time picker widgets include:
- Calendar-based date selection
- Time input with dropdowns
- Support for different date formats
- Validation for date ranges

## Custom Widget Registry

PyGUIzer provides an extensible widget registry that allows you to register custom mappings for your own types:

```python
from pyguizer.core.widget import register_widget_mapping, WidgetType
from your_library import CustomType

def custom_widget_generator(py_type):
    return WidgetType.JSON, {"description": "Custom type editor"}

# Register with priority
register_widget_mapping(CustomType, custom_widget_generator, priority=10)

# Usage
from pyguizer import PyGUIzer

@app
def process_data(custom_input: CustomType) -> str:
    return f"Processed: {custom_input}"
```

### Registry Features

- Multiple mapping types: direct, inheritance-based, string-based
- Priority levels for resolving conflicts
- Support for third-party library classes
- Easy-to-use API for registration
