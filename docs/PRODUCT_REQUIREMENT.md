# PyGUIzer - Python Function to Web GUI Generator

## 1. Overview & Vision
**PyGUIzer** is an open-source framework that automatically generates interactive, production-ready web GUI applications from standard Python function signatures. It enables developers, data scientists, and engineers to instantly productize scripts, tools, and algorithms as shareable web services or desktop applications with zero frontend code.

**Vision:** To become the de facto standard for rapid, beautiful, and deployable interface generation for the Python ecosystem, bridging the gap between Python’s powerful backend logic and accessible user interfaces.

## 2. Problem Statement
Converting a Python script or function into a usable tool for non-technical stakeholders is a major friction point. Existing solutions present difficult choices:
*   **Building a full web app** (e.g., with Streamlit, Dash) requires learning a specific framework and often mixes UI logic with business logic.
*   **Using native GUI toolkits** (e.g., PySide6) involves a steep learning curve, platform-specific considerations, and outdated aesthetics.
*   **Manual packaging and distribution** of command-line tools creates high usage barriers.

There is a gap for a tool that is as simple as adding a decorator, yet as powerful and customizable as a full-stack framework, supporting modern needs like async tasks, real-time updates, and flexible deployment.

## 3. Product Goals
1.  **Intuitive Abstraction:** Generate a complete GUI from a function signature and type hints alone.
2.  **Developer Experience First:** Prioritize a "vibe coding" workflow, where AI assistants can easily reason about and extend the codebase.
3.  **Production-Ready:** Built-in support for state management, validation, async operations, and scalable deployment.
4.  **Full Customization:** Escape the "walled garden" – provide hooks to customize every aspect of the UI, layout, and behavior.
5.  **Open & Extensible:** Foster a community-driven ecosystem for custom widgets, themes, and integrations.

## 4. Competitive Analysis & Strategic Positioning
The competitive landscape consists of adjacent tools, but none directly solve the core problem with PyGUIzer's philosophy.

| Tool / Category              | Key Strengths                                                | Key Limitations                                              | PyGUIzer’s Strategic Differentiation                         |
| :--------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Streamlit / Gradio**       | Rapid prototyping, data-science focused, huge adoption.      | Limited UI customization, app structure can become messy, primarily web-only. | **Deep customization & flexibility.** Our declarative layout config and escape hatches to direct frontend code cater to complex, product-grade apps. |
| **v0.dev / AI UI Gen**       | “Vibe coding” for React components, excellent for UI iteration. | Generates frontend code only, not a full-stack Python app. Requires React/JS knowledge to integrate backend. | **Full-stack automation.** We generate the *entire working application* from backend logic to served UI, abstracting away the frontend entirely. |
| **Electron/Tauri + GUI Lib** | Ultimate control, desktop-native, cross-platform.            | Very high complexity. Requires managing separate frontend/backend codebases, build processes, and IPC. | **Zero frontend knowledge.** Removes the entire frontend development burden while still allowing export to these frameworks for distribution. |
| **PySide6 / Qt**             | Native, powerful, great for complex desktop software.        | Verbose, non-web, difficult to style, steep learning curve.  | **Web-tech advantages.** Leverages modern web UI aesthetics, CSS, and easy remote access. Lowers the barrier to creation significantly. |
| **Framer / Webflow**         | Exceptional visual and interaction design for the web.       | Design/development hybrids. Not designed to wrap arbitrary Python business logic. | **Python-backend centric.** We start from the function (the business value) and build the UI around it, not the other way around. |

**Key Insight:** Existing tools either own the UI layer completely (limiting customization) or own neither layer (requiring heavy integration). **PyGUIzer’s unique position is to own the *integration layer* completely**, providing a seamless, declarative bridge between Python and a customizable, standards-based web frontend, giving developers full control back when needed.

## 5. Core User Personas & Stories
**Persona 1: Data Scientist (Sofia)**
*   **Story:** “I have a model inference function with parameters (file upload, confidence threshold). I need to share it with my product team for testing in under 10 minutes.”
*   **Requirement:** Auto-detection of `Path` (for upload), `float` (for slider), clean display of results.

**Persona 2: DevOps Engineer (Mark)**
*   **Story:** “I’ve written a dozen Python scripts for server management. I want a secure, internal web dashboard to run them, with logs, and job queues.”
*   **Requirement:** Async execution, real-time log streaming (`StreamingResponse`), authentication hooks, and preset configurations for different environments.

**Persona 3: Independent Developer (Alex)**
*   **Story:** “I’m building a niche desktop tool for video processing. I need a GUI that looks modern, can be packaged for Windows/macOS, and is easy to update.”
*   **Requirement:** Custom theming (dark/light), layout control, packaging to a standalone binary using Tauri or Electron, and updater support.

## 6. Detailed Functional Requirements

**FR1: Core Function-to-UI Mapping**
*   The library must introspect a Python function’s signature, docstring, and **type hints**.
*   It must map standard types (`str`, `int`, `float`, `bool`, `List`, `Dict`, `Optional`, `Union`, `Enum`) to appropriate rich UI widgets (input, slider, checkbox, multi-select, JSON editor, etc.).
*   It must support **extended types** like `Path` (file upload), `Color` (color picker), and `datetime` (date/time picker).

**FR2: Declarative UI & Layout Configuration**
*   Users must be able to override auto-generated layouts via a **Python dict or YAML** configuration.
*   Configuration must support **grouping controls** into tabs, accordions, and sections.
*   It must allow for **customizing widget properties** (e.g., slider min/max, placeholder text).
*   The generated UI must be fully **responsive** and support custom **themes (light/dark)**.

**FR3: Advanced Execution & State Management**
*   The framework must **seamlessly support async functions**.
*   It must provide built-in mechanisms for **long-running tasks**, including:
    *   Progress bar updates sent from the backend.
    *   Real-time, **streaming text/output** (e.g., for logs).
    *   Execution state locking to prevent duplicate submissions.
*   It must **automatically validate** input against type hints and provide in-UI error feedback.
*   It must **cache previous user inputs** locally (per session/browser).
*   It must support saving and loading **named preset configurations**.

**FR4: Deployment & Integration Flexibility**
*   The primary output must be a **standalone FastAPI** application that can be run directly.
*   It must expose an API router that can be **mounted into any existing FastAPI/Starlette** app.
*   It must provide a build command to generate a **standalone desktop binary** using a lightweight webview framework (e.g., Tauri for minimal size) or Electron for maximum compatibility.
*   The architecture must cleanly separate the frontend from the backend API, allowing for custom frontend builds.

## 7. Non-Functional Requirements
*   **Performance:** UI must feel instant. Async endpoints must not block the server.
*   **Security:** Input validation is mandatory. The design must discourage (or make explicit) the exposure of unsafe functions.
*   **Developer Experience:** The API must be intuitive. The codebase must be well-typed to maximize the efficacy of AI coding assistants (GitHub Copilot, Cursor).
*   **Extensibility:** The widget mapping system must be modular, allowing users to register custom type-to-widget converters.

## 8. Technical Architecture Outline (High-Level)
*   **Backend (Python):** Built on **FastAPI** for its async support, automatic OpenAPI generation, and ease of use. Uses Pydantic for robust validation and settings management.
*   **Frontend (TypeScript/React):** A **decoupled React** application that consumes the auto-generated OpenAPI spec. Uses a component library like **Shadcn/ui** or MUI for clean, customizable components. The frontend is packaged as static assets served by the backend.
*   **Communication:** Standard REST API for most operations, with **WebSocket** support for real-time features like progress streaming.
*   **Packaging:** A CLI tool will handle bundling the Python backend and frontend assets into a desktop binary using **Tauri** as the primary target due to its small bundle size and security focus.
