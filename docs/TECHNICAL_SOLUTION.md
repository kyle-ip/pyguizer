# PyGUIzer Technical Architecture & Design Specification

**Document Version:** 1.0
**Audience:** Engineering Leads, Core Contributors

---

## **1. Executive Summary & Architectural Philosophy**

PyGUIzer is architected around a clear separation of concerns between a **declarative backend specification** and a **dynamic, standards-based frontend**. Its core innovation is not a new widget library, but an **intelligent, bidirectional bridge** between Python's type ecosystem and a reactive web UI. The system prioritizes **convention over configuration** for the 80% use case, while providing **explicit escape hatches** for full customization of the remaining 20%. The architecture is designed to be statically analyzable to maximize compatibility with AI-assisted "vibe coding" workflows.

## **2. High-Level System Architecture**

The system follows a **client-server model** with a clear API contract.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                             PyGUIzer Application                                                                                                  │
├───────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  Client-Side  │           Server-Side                                                                                                                           │
│  (Browser)    │  (Python Runtime)                                                                                                                               │
│               │                                                                                                                                                 │
│  ┌────────────┴─────────┐  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐                           │
│  │  React App           │◄─┤  FastAPI Server                                                                                         │                           │
│  │  - Function Sidebar   │  │  - OpenAPI Gen                                                                                          │                           │
│  │  - Drag & Drop UI     │  │  - Request Routing                                                                                      │                           │
│  │  - Multi-function UI  │  - Auth/Session                                                                                      │                           │
│  │  - Multi-function UI  │  │  - WebSocket Support                                                                                  │                           │
│  │  - Real-time Updates  │  └──────────────────────────────────────────┬───────────────────────────────────────────────────────────┘                           │
│  └────────────┬─────────┘                                              │                                                                                       │
│               │  HTTP/WS                                               │                                                                                       │
├───────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│               │  ┌──────────────────────────────────────────────────────┴───────────────────────────────────────────────────────────┐                           │
│               └─►│  PyGUIzer Core Engine                                                                                        │◄────────────────────────────┘
│                  │  - Function Registry                                                                                          │          │
│                  │  - Type-to-Widget Resolution                                                                                  │          │
│                  │  - Layout Engine                                                                                              │          │
│                  │  - Task Orchestrator                                                                                          │          │
│                  │  - Task Orchestrator                                                                                          │          │
│                  └──────────────────────────────────────────┬───────────────────────────────────────────────────────────┘          │
│                                                           │                                                                       │
│                  ┌──────────────────────────────────────────┴───────────────────────────────────────────────────────────┐          │
│                  │  Extension Registry                                                                                        │          │
│                  │  - Custom Widgets                                                                                          │          │
│                  │  - Theme Packs                                                                                             │          │
│                  │  - Deployment Adapters                                                                                     │          │
│                  └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Key Design Tenets:**
1.  **API-First:** The backend exposes a clean, versioned REST & WebSocket API. The default frontend is one possible consumer.
2.  **Loose Coupling:** The frontend (React) communicates solely via the auto-generated OpenAPI schema. It can be replaced entirely.
3.  **Extensible Core:** A registry pattern allows for pluggable components (widgets, themes, deployment targets).
4.  **Multi-function Architecture:** The system is designed from the ground up to support multiple functions and their independent execution.

## **3. Core Component Detailed Design**

### **3.1. Type Introspection & Widget Mapping Engine**
This is the heart of PyGUIzer. It transforms a Python callable into a UI schema.

*   **Process Flow:**
    1.  **Inspection:** Uses `inspect.signature` and `typing.get_type_hints` to extract parameters, types, defaults, and docstrings.
    2.  **Resolution:** Navigates through `Union`, `Optional`, `List`, `Dict`, and generic types. Recognizes custom "marker" types (e.g., `Path`, `Color`).
    3.  **Schema Generation:** For each parameter, creates a **Widget Specification Object (WSO)**. This is a JSON-serializable dict containing:
        *   `id`: Derived from the parameter name.
        *   `type`: Internal widget type (e.g., `"number_slider"`, `"file_upload"`).
        *   `dataType`: Original Python type (`"int"`, `"List[str]"`).
        *   `label`: Generated from parameter name or extracted from docstring.
        *   `default`: The parameter's default value.
        *   `constraints`: Min/max, regex patterns, file accept types derived from type hints or function annotations (e.g., `Annotated[int, Field(ge=0, le=100)]`).
        *   `hints`: Optional guidance for the UI (e.g., `"password"`, `"multiline"`).
    4.  **Extension Point:** A global `WIDGET_REGISTRY` maps Python types or special strings to WSO generators. Users can register custom mappings: `register_widget_mapping(MyCustomClass, my_wso_generator_func)`.

### **3.2. Function Registry**
Manages all registered functions within an application.

*   **Function Registration:** Functions are registered via the `@PyGUIzer()` decorator, which adds them to a central registry.
*   **Function Metadata:** For each registered function, the registry stores:
    *   Function name and description (from docstring)
    *   Introspected parameters and return type
    *   Generated WSOs
    *   Auto-generated UI layout
*   **API:** Provides methods for:
    *   Registering/unregistering functions
    *   Getting all registered functions
    *   Getting function details by name

### **3.3. Declarative Layout Engine**
Transforms a flat list of WSOs into a structured UI layout.

*   **Layout Specification:** A hierarchical JSON/YAML/Python-dict structure defining `sections`, `tabs`, `rows`, and `columns`. It references WSO `id`s.
*   **Two-Phase Processing:**
    1.  **Validation:** Ensures all referenced WSO `id`s exist and layout rules are consistent.
    2.  **Enrichment:** Merges the layout spec with the WSO list. A WSO not mentioned in the layout is placed in a default "Other" section.
*   **Multi-function Support:** Handles layouts for multiple functions simultaneously, with each function having its own independent layout.
*   **Output:** A **UI Layout Schema** consumed by the frontend to render the navigation and group controls.

### **3.4. Asynchronous Task Orchestrator**
Manages long-running function executions.

*   **State Model:** Each execution is a `Task` with states: `PENDING`, `RUNNING`, `STREAMING`, `SUCCESS`, `FAILED`, `CANCELLED`.
*   **Abstraction Layer:** Uses a pluggable backend. For development: an in-memory `BackgroundTaskManager`. For production: a Celery + Redis or RQ (Redis Queue) adapter.
*   **Communication Channels:**
    *   **REST Endpoint:** To submit tasks and poll for final results.
    *   **WebSocket Connection:** Established per-task for real-time, bidirectional communication.
        *   **Downstream (Server -> Client):** Sends progress updates (`%`, message), streaming stdout/stderr chunks, and final results.
        *   **Upstream (Client -> Server):** Can send cancellation signals.
*   **Function Wrapping:** The `@async_task` decorator injects a `progress_callback` and `stream_writer` object into the wrapped function, providing a clean API for the developer to report state.

### **3.5. Frontend Application (Reference Implementation)**
A React/TypeScript SPA that dynamically builds itself from the API schema.

*   **State Management (Zustand):** Central stores for:
    *   `AppState`: Layout schema, theme, presets, registered functions.
    *   `InputState`: Current values of all UI controls, validation errors.
    *   `TaskState`: Map of active/past tasks and their status.
*   **Main Components:**
    *   **Function Sidebar:** Displays all registered functions with their names and descriptions
    *   **Central Execution Panel:** Displays function UIs for the selected function
    *   **Widget Factory:** A component that reads a WSO and renders the corresponding React component (e.g., `NumberSlider`, `JsonEditor`)
*   **Real-Time Service:** Manages WebSocket connections, subscribes to task channels, and updates the state stores.

## **4. Data Models & API Contracts**

### **4.1. Primary Data Models**
*   `AppSpec`: The complete configuration (function metadata, WSO list, layout, theme, registered functions).
*   `WidgetSpec`: As defined in 3.1.
*   `Task`: `{id: str, status: Enum, created_at: datetime, result?: any, error?: string}`.
*   `Preset`: `{name: str, description?: str, values: Dict[str, any]}`.
*   `FunctionInfo`: `{name: str, display_name: str, description: str, parameters: List[WidgetSpec], return_type: str}`.

### **4.2. Core API Endpoints**
*   `GET /api/spec` -> Returns the `AppSpec`. This bootstraps the frontend.
*   `GET /api/functions` -> Returns all registered functions.
*   `GET /api/functions/{function_name}` -> Returns details for a specific function.
*   `POST /api/run` -> Submits inputs, starts a task, returns a `Task` ID.
*   `GET /api/tasks/{task_id}` -> Polls for task status/result.
*   `GET /api/tasks/{task_id}/stream` -> **WebSocket endpoint** for real-time updates.
*   `GET /api/presets`, `POST /api/presets` -> Manage saved presets.
*   `POST /api/validate/{widget_id}` (Optional) - For real-time field validation.

## **5. Cross-Cutting Concerns**

*   **Error Handling:** Structured error responses (HTTP codes + JSON body). Unhandled exceptions in user callbacks are caught and presented as task failures with sanitized messages.
*   **Validation:** Two-tiered: 1) Frontend validation from WSO constraints for UX. 2) Backend Pydantic validation before execution for security.
*   **Persistence:** For presets and input cache, a lightweight SQLite store is used by default. An interface allows adapters for other databases (PostgreSQL).
*   **Security:**
    *   Input sanitization is enforced by Pydantic.
    *   File uploads are sandboxed to a temp directory with size limits.
    *   The library will include clear warnings about exposing unsafe functions (e.g., `os.system`, `eval`) and provide decorators to restrict their execution in production mode.
*   **Theming:** Uses CSS-in-JS (Emotion) or Tailwind with a CSS variable-based theme system (`--primary-color`, `--border-radius`). Themes are config files that set these variables.
*   **Performance:** Optimized for handling multiple concurrent function executions. Includes caching of function introspection results.

## **6. Packaging & Deployment Subsystem**

This is a key competitive differentiator. The system uses a plugin architecture for `DeploymentTarget`s.

1.  **FastAPI Server (Default):** Packages the app into a standard ASGI app with all registered functions.
2.  **Standalone Binary (Tauri Target):**
    *   **Builder:** Invokes the Tauri CLI via a Python subprocess.
    *   **Process:** Bundles the backend, frontend assets, and a minimal Rust wrapper into a single binary for Windows, macOS, and Linux.
3.  **Docker Container:** Generates a production-optimized Dockerfile with multistage build, non-root user, and health checks.
4.  **Framework Integration (FastAPI/Flask Plugin):** Exports the `PyGUIzer` instance as a router/blueprint that can be mounted into a larger existing application.

## **7. Development & Build Tooling**

*   **CLI Tool (`pyguizer`):** For project scaffolding, building, and deployment.
    *   `pyguizer init`: Creates a new project with `app.py` and layout config.
    *   `pyguizer run`: Starts the dev server with hot reload.
    *   `pyguizer build --target tauri`: Builds for the specified target.
    *   `pyguizer functions`: Lists all registered functions.
*   **Code Generation:** For advanced use cases, a command can generate the React frontend as source code, allowing developers to "eject" and take full control.

## **8. Implementation Roadmap (Phased)**

**Phase 1: Foundational Core (Weeks 1-6)**
*   Basic type introspection & WSO generation for standard types.
*   Simple React frontend with static widget set.
*   Synchronous execution via FastAPI.
*   Basic layout config (sections).

**Phase 2: Enhanced Experience (Weeks 7-12)**
*   Async task orchestration with WebSocket streaming.
*   Advanced type support (`Path`, `Dict`) and custom widget registry.
*   Preset management and input caching.
*   Tauri binary packaging.

**Phase 3: Production & Ecosystem (Weeks 13-18)**
*   Comprehensive auth/security plugins.
*   Advanced layout engine (drag-and-drop designer as a separate app).
*   Deployment adapters (Docker, Desktop installers).
*   Performance optimization and comprehensive documentation.
*   Enhanced layout system with tabs, accordions, and grid layouts.

**Phase 4: Multi-function Support (Weeks 19-24)**
*   **Function Registry:** Implement support for registering multiple functions
*   **Frontend Redesign:** Update frontend to include sidebar and function selection
*   **API Enhancements:** Add endpoints for function management
*   **Testing:** Comprehensive testing of multi-function features
