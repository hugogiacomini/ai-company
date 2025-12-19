"""
Backend abstraction layer for AI Company simulation.
Provides a unified interface for both CrewAI and Claude Code backends.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class BackendType(str, Enum):
    """Available backend types"""
    CREWAI = "crewai"
    CLAUDE_CODE = "claude_code"


class AgentRole(BaseModel):
    """Unified agent role representation across backends"""
    role: str = Field(description="Agent role title")
    goal: str = Field(description="Agent's primary goal")
    backstory: str = Field(description="Agent's background and expertise")
    department: str = Field(description="Department the agent belongs to")
    level: str = Field(description="Hierarchy level (executive, head, specialist, etc.)")
    can_delegate: bool = Field(description="Whether agent can delegate tasks")
    skills: List[str] = Field(default_factory=list, description="Agent's skills")
    tools: Optional[List[str]] = Field(None, description="Tools available to the agent")


class TaskDefinition(BaseModel):
    """Unified task representation across backends"""
    description: str = Field(description="Task description")
    agent_role: str = Field(description="Role of agent assigned to this task")
    expected_output: str = Field(description="Expected output format")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context for task")
    depends_on: List[str] = Field(default_factory=list, description="Task IDs this task depends on")
    task_id: Optional[str] = Field(None, description="Unique task identifier")


class WorkflowResult(BaseModel):
    """Unified workflow result representation"""
    success: bool = Field(description="Whether workflow completed successfully")
    outputs: Dict[str, Any] = Field(description="Workflow outputs by agent/task")
    metadata: Dict[str, Any] = Field(description="Additional metadata about execution")


class BaseBackend(ABC):
    """
    Abstract base class for agent execution backends.

    Implementations must provide methods for:
    - Initializing the backend
    - Creating agents from role definitions
    - Creating tasks from task definitions
    - Executing workflows with agents and tasks
    """

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the backend with configuration.

        Args:
            config: Backend-specific configuration parameters
        """
        pass

    @abstractmethod
    def create_agent(self, agent_def: AgentRole) -> Any:
        """
        Create an agent in the backend from an agent definition.

        Args:
            agent_def: Unified agent role definition

        Returns:
            Backend-specific agent object
        """
        pass

    @abstractmethod
    def create_task(self, task_def: TaskDefinition) -> Any:
        """
        Create a task in the backend from a task definition.

        Args:
            task_def: Unified task definition

        Returns:
            Backend-specific task object
        """
        pass

    @abstractmethod
    def execute_workflow(
        self,
        agents: List[Any],
        tasks: List[Any],
        process_type: str = "sequential"
    ) -> WorkflowResult:
        """
        Execute a workflow with the given agents and tasks.

        Args:
            agents: List of backend-specific agent objects
            tasks: List of backend-specific task objects
            process_type: Workflow execution mode ("sequential" or "parallel")

        Returns:
            WorkflowResult with execution results and metadata
        """
        pass

    @abstractmethod
    def supports_parallel_execution(self) -> bool:
        """
        Check if this backend supports parallel task execution.

        Returns:
            True if parallel execution is supported, False otherwise
        """
        pass

    @abstractmethod
    def get_backend_type(self) -> BackendType:
        """
        Return the backend type identifier.

        Returns:
            BackendType enum value
        """
        pass

    def cleanup(self) -> None:
        """
        Optional cleanup method called when backend is no longer needed.
        Subclasses can override to perform cleanup operations.
        """
        pass
