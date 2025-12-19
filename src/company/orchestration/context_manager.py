"""
Context manager for sharing information between agents in workflows.
Enables agents to build on each other's outputs.
"""
from typing import Dict, Any, List, Optional


class ContextManager:
    """
    Manages context sharing between agents in multi-agent workflows.

    Stores task results and makes them available to dependent tasks,
    enabling agents to build on each other's work.
    """

    def __init__(self):
        """Initialize the context manager"""
        self.context_store: Dict[str, Dict[str, Any]] = {}
        self.task_results: Dict[str, Any] = {}
        self.workflow_metadata: Dict[str, Any] = {}

    def add_context(self, task_id: str, context: Dict[str, Any]) -> None:
        """
        Add context for a specific task.

        Args:
            task_id: Unique task identifier
            context: Context dictionary for the task
        """
        self.context_store[task_id] = context

    def get_context(self, task_id: str) -> Dict[str, Any]:
        """
        Retrieve context for a specific task.

        Args:
            task_id: Task identifier

        Returns:
            Context dictionary, or empty dict if not found
        """
        return self.context_store.get(task_id, {})

    def store_result(self, task_id: str, result: Any) -> None:
        """
        Store the result of a completed task.

        Args:
            task_id: Task identifier
            result: Task execution result
        """
        self.task_results[task_id] = result

    def get_result(self, task_id: str) -> Optional[Any]:
        """
        Get the result of a completed task.

        Args:
            task_id: Task identifier

        Returns:
            Task result if available, None otherwise
        """
        return self.task_results.get(task_id)

    def build_context_for_task(
        self,
        task_id: str,
        dependencies: List[str],
        additional_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Build comprehensive context for a task including dependency results.

        Args:
            task_id: Task identifier
            dependencies: List of task IDs this task depends on
            additional_context: Optional additional context to include

        Returns:
            Combined context dictionary
        """
        # Start with task's own context
        context = self.get_context(task_id).copy()

        # Add results from dependency tasks
        for dep_id in dependencies:
            if dep_id in self.task_results:
                context[f"output_from_{dep_id}"] = self.task_results[dep_id]

        # Add any additional context
        if additional_context:
            context.update(additional_context)

        # Add workflow metadata if available
        if self.workflow_metadata:
            context["workflow_metadata"] = self.workflow_metadata

        return context

    def set_workflow_metadata(self, metadata: Dict[str, Any]) -> None:
        """
        Set workflow-level metadata available to all tasks.

        Args:
            metadata: Workflow metadata dictionary
        """
        self.workflow_metadata = metadata

    def get_workflow_metadata(self) -> Dict[str, Any]:
        """
        Get workflow-level metadata.

        Returns:
            Workflow metadata dictionary
        """
        return self.workflow_metadata

    def clear(self) -> None:
        """Clear all stored context and results"""
        self.context_store.clear()
        self.task_results.clear()
        self.workflow_metadata.clear()

    def get_all_results(self) -> Dict[str, Any]:
        """
        Get all task results.

        Returns:
            Dictionary of all task results by task ID
        """
        return self.task_results.copy()

    def has_result(self, task_id: str) -> bool:
        """
        Check if a task result is available.

        Args:
            task_id: Task identifier

        Returns:
            True if result exists, False otherwise
        """
        return task_id in self.task_results
