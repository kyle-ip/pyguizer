"""PyGUIzer application service"""

import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import HTTPException

from pyguizer.core.introspection import introspect_function
from pyguizer.core.layout import process_layout
from pyguizer.core.widget import generate_wso


class PyGUIzerApp:
    """Main PyGUIzer application class."""

    def __init__(
        self,
        name="PyGUIzer App",
        description="Multi-function PyGUIzer Application",
        func=None,
        layout=None,
    ):
        self.name = name
        self.description = description

        self.layout = layout or {
            "containers": [{"name": "Main", "type": "section", "widgets": []}]
        }

        # Function registry - maps function name to function metadata
        self.function_registry = {}

        # Preset management
        self.presets = []

        # Pipeline management
        self.pipelines = []

        # If a function is provided during initialization, register it
        if func:
            self.register_function(func)

    def register_function(self, func, layout=None, group="default"):
        """Register a new function with the application.

        Args:
            func: The function to register
            layout: Optional layout configuration for the function
            group: Optional group/category for the function
        """
        # Introspect the function
        func_info = introspect_function(func)

        # Generate WSOs
        wsos = generate_wso(func_info["parameters"])

        # Process layout for this function
        function_layout = process_layout(wsos, layout or self.layout)

        # Register the function
        func_name = func.__name__
        self.function_registry[func_name] = {
            "func": func,
            "func_info": func_info,
            "wsos": wsos,
            "ui_layout": function_layout,
            "group": group,
        }

    def get_app_spec(self) -> Dict[str, Any]:
        """Get the application specification."""
        # Build function specs for all registered functions
        functions = []
        function_groups = {}

        for func_name, func_data in self.function_registry.items():
            # Extract only the necessary information without complex type objects
            func_spec = {
                "name": func_name,
                "display_name": func_data["func_info"]["name"],
                "description": func_data["func_info"]["docstring"],
                "layout": func_data["ui_layout"],
                "group": func_data.get("group", "default"),
            }
            functions.append(func_spec)

            # Organize functions by group
            group = func_data.get("group", "default")
            if group not in function_groups:
                function_groups[group] = []
            function_groups[group].append(func_spec)

        return {
            "name": self.name,
            "description": self.description,
            "functions": functions,
            "function_groups": function_groups,
        }

    async def run_function(self, func_name: str, inputs: Dict[str, Any]) -> Any:
        """Run a registered function with provided inputs.

        Args:
            func_name: The name of the function to run
            inputs: The inputs to pass to the function

        Returns:
            The result of the function execution

        Raises:
            HTTPException: If the function is not found or execution fails
        """
        if func_name not in self.function_registry:
            raise HTTPException(
                status_code=404, detail=f"Function '{func_name}' not found"
            )

        func = self.function_registry[func_name]["func"]
        try:
            # Check if the function is async
            import asyncio

            if asyncio.iscoroutinefunction(func):
                return await func(**inputs)
            else:
                # Run sync function in executor
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, lambda: func(**inputs))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_presets(self) -> List[Dict[str, Any]]:
        """Get all presets."""
        return self.presets

    def create_preset(
        self, name: str, description: str, values: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new preset."""
        preset = {
            "id": str(uuid.uuid4()),
            "name": name,
            "description": description,
            "values": values,
            "created_at": time.time(),
        }
        self.presets.append(preset)
        return preset

    def get_preset(self, preset_id: str) -> Dict[str, Any]:
        """Get a preset by ID."""
        for preset in self.presets:
            if preset["id"] == preset_id:
                return preset
        raise HTTPException(status_code=404, detail="Preset not found")

    def update_preset(
        self,
        preset_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        values: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Update a preset by ID."""
        preset = self.get_preset(preset_id)
        if name is not None:
            preset["name"] = name
        if description is not None:
            preset["description"] = description
        if values is not None:
            preset["values"] = values
        preset["updated_at"] = time.time()
        return preset

    def delete_preset(self, preset_id: str) -> Dict[str, Any]:
        """Delete a preset by ID."""
        preset = self.get_preset(preset_id)
        self.presets.remove(preset)
        return {
            "status": "deleted",
            "message": f"Preset {preset_id} deleted successfully",
        }

    def get_pipelines(self):
        """Get all pipelines."""
        return self.pipelines

    def create_pipeline(self, name: str, description: str):
        """Create a new pipeline."""
        from pyguizer.api.models import Pipeline

        pipeline = Pipeline(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            nodes=[],
            connections=[],
            created_at=time.time(),
            updated_at=time.time(),
        )
        self.pipelines.append(pipeline)
        return pipeline

    def get_pipeline(self, pipeline_id: str):
        """Get a pipeline by ID."""
        for pipeline in self.pipelines:
            if pipeline.id == pipeline_id:
                return pipeline
        raise HTTPException(status_code=404, detail="Pipeline not found")

    def update_pipeline(self, pipeline_id: str, **kwargs):
        """Update a pipeline by ID."""
        pipeline = self.get_pipeline(pipeline_id)
        for key, value in kwargs.items():
            if hasattr(pipeline, key):
                setattr(pipeline, key, value)
        pipeline.updated_at = time.time()
        return pipeline

    def delete_pipeline(self, pipeline_id: str) -> Dict[str, Any]:
        """Delete a pipeline by ID."""
        pipeline = self.get_pipeline(pipeline_id)
        self.pipelines.remove(pipeline)
        return {
            "status": "deleted",
            "message": f"Pipeline {pipeline_id} deleted successfully",
        }

    def add_node_to_pipeline(self, pipeline_id: str, node_data):
        """Add a node to a pipeline."""
        from pyguizer.api.models import PipelineNode

        pipeline = self.get_pipeline(pipeline_id)

        # Validate function exists
        if node_data.function_name not in self.function_registry:
            raise HTTPException(
                status_code=404,
                detail=f"Function '{node_data.function_name}' not found",
            )

        node = PipelineNode(
            id=str(uuid.uuid4()),
            function_name=node_data.function_name,
            node_name=node_data.node_name,
            parameters=node_data.parameters,
            position=node_data.position,
        )
        pipeline.nodes.append(node)
        pipeline.updated_at = time.time()
        return node

    def update_pipeline_node(self, pipeline_id: str, node_id: str, node_data):
        """Update a pipeline node."""
        pipeline = self.get_pipeline(pipeline_id)
        for node in pipeline.nodes:
            if node.id == node_id:
                if node_data.node_name is not None:
                    node.node_name = node_data.node_name
                if node_data.parameters is not None:
                    node.parameters = node_data.parameters
                if node_data.position is not None:
                    node.position = node_data.position
                pipeline.updated_at = time.time()
                return node
        raise HTTPException(status_code=404, detail="Node not found in pipeline")

    def delete_pipeline_node(self, pipeline_id: str, node_id: str) -> Dict[str, Any]:
        """Delete a pipeline node."""
        pipeline = self.get_pipeline(pipeline_id)
        node = next((n for n in pipeline.nodes if n.id == node_id), None)
        if not node:
            raise HTTPException(status_code=404, detail="Node not found in pipeline")

        # Remove connections associated with this node
        pipeline.connections = [
            c
            for c in pipeline.connections
            if c.source_node_id != node_id and c.target_node_id != node_id
        ]

        pipeline.nodes.remove(node)
        pipeline.updated_at = time.time()
        return {
            "status": "deleted",
            "message": f"Node {node_id} deleted successfully from pipeline",
        }

    def add_connection_to_pipeline(self, pipeline_id: str, connection_data):
        """Add a connection to a pipeline."""
        from pyguizer.api.models import PipelineConnection

        pipeline = self.get_pipeline(pipeline_id)

        # Validate source and target nodes exist
        source_node = next(
            (n for n in pipeline.nodes if n.id == connection_data.source_node_id), None
        )
        target_node = next(
            (n for n in pipeline.nodes if n.id == connection_data.target_node_id), None
        )

        if not source_node:
            raise HTTPException(
                status_code=404, detail="Source node not found in pipeline"
            )
        if not target_node:
            raise HTTPException(
                status_code=404, detail="Target node not found in pipeline"
            )

        # Validate function parameters
        target_func = self.function_registry[target_node.function_name]

        # Check if target input exists
        target_param_names = [p["name"] for p in target_func["func_info"]["parameters"]]
        if connection_data.target_input not in target_param_names:
            raise HTTPException(
                status_code=400,
                detail=f"Target input '{connection_data.target_input}' not found "
                f"in function '{target_node.function_name}'",
            )

        connection = PipelineConnection(
            id=str(uuid.uuid4()),
            source_node_id=connection_data.source_node_id,
            source_output=connection_data.source_output,
            target_node_id=connection_data.target_node_id,
            target_input=connection_data.target_input,
        )

        # Check for cyclic dependencies
        if self._has_cyclic_dependency(pipeline, connection):
            raise HTTPException(
                status_code=400, detail="Connection would create a cyclic dependency"
            )

        pipeline.connections.append(connection)
        pipeline.updated_at = time.time()
        return connection

    def delete_pipeline_connection(
        self, pipeline_id: str, connection_id: str
    ) -> Dict[str, Any]:
        """Delete a pipeline connection."""
        pipeline = self.get_pipeline(pipeline_id)
        connection = next(
            (c for c in pipeline.connections if c.id == connection_id), None
        )
        if not connection:
            raise HTTPException(
                status_code=404, detail="Connection not found in pipeline"
            )

        pipeline.connections.remove(connection)
        pipeline.updated_at = time.time()
        return {
            "status": "deleted",
            "message": f"Connection {connection_id} deleted successfully from pipeline",
        }

    def _has_cyclic_dependency(self, pipeline, new_connection=None) -> bool:
        """Check if adding a connection would create a cyclic dependency."""
        # Build adjacency list
        adjacency = {node.id: [] for node in pipeline.nodes}

        # Add existing connections
        for connection in pipeline.connections:
            adjacency[connection.source_node_id].append(connection.target_node_id)

        # Add new connection if provided
        if new_connection:
            adjacency[new_connection.source_node_id].append(
                new_connection.target_node_id
            )

        # Check for cycles using DFS
        visited = set()
        rec_stack = set()

        def has_cycle(node_id):
            if node_id not in visited:
                visited.add(node_id)
                rec_stack.add(node_id)

                for neighbor in adjacency.get(node_id, []):
                    if neighbor not in visited:
                        if has_cycle(neighbor):
                            return True
                    elif neighbor in rec_stack:
                        return True

                rec_stack.remove(node_id)
            return False

        for node_id in adjacency:
            if has_cycle(node_id):
                return True

        return False

    def validate_pipeline(self, pipeline_id: str) -> Dict[str, Any]:
        """Validate a pipeline configuration."""
        pipeline = self.get_pipeline(pipeline_id)

        # Check for cyclic dependencies
        if self._has_cyclic_dependency(pipeline):
            return {
                "valid": False,
                "errors": ["Pipeline contains cyclic dependencies"],
            }

        # Check for disconnected nodes
        connected_nodes = set()
        for connection in pipeline.connections:
            connected_nodes.add(connection.source_node_id)
            connected_nodes.add(connection.target_node_id)

        disconnected_nodes = [
            node.node_name
            for node in pipeline.nodes
            if node.id not in connected_nodes and len(pipeline.connections) > 0
        ]

        errors = []
        if disconnected_nodes:
            errors.append(f"Disconnected nodes: {', '.join(disconnected_nodes)}")

        # Check node function validity
        for node in pipeline.nodes:
            if node.function_name not in self.function_registry:
                errors.append(
                    f"Node '{node.node_name}' references non-existent function "
                    f"'{node.function_name}'"
                )

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": disconnected_nodes if disconnected_nodes else [],
        }

    async def execute_pipeline(
        self, pipeline_id: str, execution_mode, run_async: bool = True
    ):
        """Execute a pipeline."""
        pipeline = self.get_pipeline(pipeline_id)

        # Validate pipeline
        validation = self.validate_pipeline(pipeline_id)
        if not validation["valid"]:
            raise HTTPException(
                status_code=400,
                detail=f"Pipeline validation failed: {'; '.join(validation['errors'])}",
            )

        # Build execution graph
        node_map = {node.id: node for node in pipeline.nodes}
        connections = pipeline.connections

        # Build dependency graph
        dependencies = {node.id: [] for node in pipeline.nodes}
        reverse_dependencies = {node.id: [] for node in pipeline.nodes}

        for connection in connections:
            dependencies[connection.target_node_id].append(connection.source_node_id)
            reverse_dependencies[connection.source_node_id].append(
                connection.target_node_id
            )

        # Topological sort
        sorted_nodes = self._topological_sort(dependencies)

        # Execute nodes
        node_results = {}

        if execution_mode == "serial":
            # Serial execution
            for node_id in sorted_nodes:
                node = node_map[node_id]
                # Get inputs from dependencies
                inputs = node.parameters.copy()

                # Collect inputs from connected nodes
                for connection in connections:
                    if connection.target_node_id == node_id:
                        source_node_id = connection.source_node_id
                        if source_node_id in node_results:
                            source_result = node_results[source_node_id]
                            # Handle different output types
                            if connection.source_output == "result":
                                inputs[connection.target_input] = source_result
                            elif (
                                isinstance(source_result, dict)
                                and connection.source_output in source_result
                            ):
                                inputs[connection.target_input] = source_result[
                                    connection.source_output
                                ]

                # Execute node function
                result = await self.run_function(node.function_name, inputs)
                node_results[node_id] = result

        elif execution_mode == "parallel":
            # Parallel execution using topological levels
            levels = self._build_execution_levels(dependencies, sorted_nodes)

            for level in levels:
                # Execute all nodes in this level concurrently
                level_tasks = []

                async def execute_node_level(node_id):
                    node = node_map[node_id]
                    # Get inputs from dependencies
                    inputs = node.parameters.copy()

                    # Collect inputs from connected nodes
                    for connection in connections:
                        if connection.target_node_id == node_id:
                            source_node_id = connection.source_node_id
                            if source_node_id in node_results:
                                source_result = node_results[source_node_id]
                                # Handle different output types
                                if connection.source_output == "result":
                                    inputs[connection.target_input] = source_result
                                elif (
                                    isinstance(source_result, dict)
                                    and connection.source_output in source_result
                                ):
                                    inputs[connection.target_input] = source_result[
                                        connection.source_output
                                    ]

                    # Execute node function
                    result = await self.run_function(node.function_name, inputs)
                    node_results[node_id] = result
                    return node_id, result

                # Create tasks for all nodes in the level
                for node_id in level:
                    level_tasks.append(execute_node_level(node_id))

                # Run tasks concurrently
                import asyncio

                await asyncio.gather(*level_tasks)

        return {
            "status": "completed",
            "results": node_results,
            "node_count": len(pipeline.nodes),
            "execution_mode": execution_mode,
        }

    def _topological_sort(self, dependencies):
        """Perform topological sorting on the dependency graph."""
        # Kahn's algorithm
        in_degree = {node_id: len(deps) for node_id, deps in dependencies.items()}
        queue = [node_id for node_id, degree in in_degree.items() if degree == 0]
        top_order = []

        while queue:
            node_id = queue.pop(0)
            top_order.append(node_id)

            # For all neighbors (nodes that depend on this node)
            for neighbor in [n for n, deps in dependencies.items() if node_id in deps]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return top_order

    def _build_execution_levels(self, dependencies, sorted_nodes):
        """Build execution levels for parallel execution."""
        levels = []
        level_map = {}

        # Assign levels based on longest path from root
        for node_id in sorted_nodes:
            max_level = -1
            for dep_id in dependencies[node_id]:
                if dep_id in level_map and level_map[dep_id] > max_level:
                    max_level = level_map[dep_id]
            level = max_level + 1
            level_map[node_id] = level

            # Ensure level list exists
            while len(levels) <= level:
                levels.append([])

            levels[level].append(node_id)

        return levels
