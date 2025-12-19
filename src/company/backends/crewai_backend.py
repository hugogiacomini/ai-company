"""
CrewAI backend implementation.
Wraps CrewAI framework to implement the BaseBackend interface.
"""
from typing import Dict, Any, List
from crewai import Agent, Task, Crew, Process

from .base import BaseBackend, BackendType, AgentRole, TaskDefinition, WorkflowResult


class CrewAIBackend(BaseBackend):
    """CrewAI implementation of the backend interface"""

    def __init__(self):
        self._agents_cache: Dict[str, Agent] = {}
        self._config: Dict[str, Any] = {}

    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize CrewAI backend with configuration.

        Args:
            config: Configuration dict with optional 'verbose' key
        """
        self._config = config
        self._agents_cache.clear()

    def create_agent(self, agent_def: AgentRole) -> Agent:
        """
        Create a CrewAI Agent from AgentRole definition.

        Args:
            agent_def: Unified agent role definition

        Returns:
            CrewAI Agent object
        """
        agent = Agent(
            role=agent_def.role,
            goal=agent_def.goal,
            backstory=agent_def.backstory,
            verbose=self._config.get('verbose', True),
            allow_delegation=agent_def.can_delegate,
            max_iter=5 if agent_def.can_delegate else 3
        )

        # Cache agent for task creation
        self._agents_cache[agent_def.role] = agent

        return agent

    def create_task(self, task_def: TaskDefinition) -> Task:
        """
        Create a CrewAI Task from TaskDefinition.

        Args:
            task_def: Unified task definition

        Returns:
            CrewAI Task object

        Raises:
            ValueError: If agent for this task hasn't been created yet
        """
        # Retrieve agent from cache
        agent = self._agents_cache.get(task_def.agent_role)
        if not agent:
            raise ValueError(
                f"Agent '{task_def.agent_role}' not found. "
                f"Create agent before creating tasks."
            )

        return Task(
            description=task_def.description,
            agent=agent,
            expected_output=task_def.expected_output
        )

    def execute_workflow(
        self,
        agents: List[Agent],
        tasks: List[Task],
        process_type: str = "sequential"
    ) -> WorkflowResult:
        """
        Execute CrewAI workflow with agents and tasks.

        Args:
            agents: List of CrewAI Agent objects
            tasks: List of CrewAI Task objects
            process_type: Execution mode ("sequential" or "hierarchical")

        Returns:
            WorkflowResult with execution results and metadata
        """
        # Map process type
        process = Process.sequential if process_type == "sequential" else Process.hierarchical

        # Create and execute crew
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=process,
            verbose=self._config.get('verbose', True)
        )

        try:
            result = crew.kickoff()

            return WorkflowResult(
                success=True,
                outputs={"result": result},
                metadata={
                    "backend": "crewai",
                    "agents_count": len(agents),
                    "tasks_count": len(tasks),
                    "process": process_type
                }
            )
        except Exception as e:
            return WorkflowResult(
                success=False,
                outputs={"error": str(e)},
                metadata={
                    "backend": "crewai",
                    "agents_count": len(agents),
                    "tasks_count": len(tasks),
                    "process": process_type,
                    "error_type": type(e).__name__
                }
            )

    def supports_parallel_execution(self) -> bool:
        """
        CrewAI uses sequential execution by default.

        Returns:
            False (CrewAI doesn't support true parallel execution)
        """
        return False

    def get_backend_type(self) -> BackendType:
        """
        Return the backend type.

        Returns:
            BackendType.CREWAI
        """
        return BackendType.CREWAI

    def cleanup(self) -> None:
        """Clean up cached agents"""
        self._agents_cache.clear()
