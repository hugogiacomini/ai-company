"""Tests for base backend interfaces"""
import pytest
from src.company.backends.base import (
    AgentRole,
    TaskDefinition,
    WorkflowResult,
    BackendType
)


class TestAgentRole:
    """Test AgentRole model"""

    def test_agent_role_creation(self):
        """Test creating an agent role"""
        agent = AgentRole(
            role="Test Agent",
            goal="Test goal",
            backstory="Test backstory",
            department="test",
            level="expert",
            can_delegate=False,
            skills=["skill1", "skill2"]
        )

        assert agent.role == "Test Agent"
        assert agent.goal == "Test goal"
        assert agent.department == "test"
        assert agent.can_delegate is False
        assert len(agent.skills) == 2

    def test_agent_role_with_tools(self):
        """Test agent role with custom tools"""
        agent = AgentRole(
            role="Developer",
            goal="Write code",
            backstory="Experienced developer",
            department="software_development",
            level="senior",
            can_delegate=True,
            skills=["python", "javascript"],
            tools=["Read", "Write", "Edit", "Bash"]
        )

        assert agent.tools == ["Read", "Write", "Edit", "Bash"]

    def test_agent_role_defaults(self):
        """Test agent role with default values"""
        agent = AgentRole(
            role="Analyst",
            goal="Analyze data",
            backstory="Data analyst",
            department="operations",
            level="analyst",
            can_delegate=False,
            skills=[]
        )

        assert agent.tools is None
        assert agent.skills == []


class TestTaskDefinition:
    """Test TaskDefinition model"""

    def test_task_definition_creation(self):
        """Test creating a task definition"""
        task = TaskDefinition(
            description="Test task",
            agent_role="Test Agent",
            expected_output="Test output"
        )

        assert task.description == "Test task"
        assert task.agent_role == "Test Agent"
        assert task.expected_output == "Test output"
        assert task.context == {}
        assert task.depends_on == []

    def test_task_definition_with_context(self):
        """Test task definition with context"""
        task = TaskDefinition(
            description="Complex task",
            agent_role="Senior Developer",
            expected_output="Code implementation",
            context={"language": "python", "framework": "django"},
            depends_on=["task_1", "task_2"]
        )

        assert task.context["language"] == "python"
        assert len(task.depends_on) == 2
        assert "task_1" in task.depends_on


class TestWorkflowResult:
    """Test WorkflowResult model"""

    def test_workflow_result_success(self):
        """Test successful workflow result"""
        result = WorkflowResult(
            success=True,
            outputs={"agent1": "output1", "agent2": "output2"},
            metadata={"backend": "crewai", "duration": 10.5}
        )

        assert result.success is True
        assert len(result.outputs) == 2
        assert result.metadata["backend"] == "crewai"

    def test_workflow_result_failure(self):
        """Test failed workflow result"""
        result = WorkflowResult(
            success=False,
            outputs={"error": "Task failed"},
            metadata={"backend": "claude_code", "error_type": "TimeoutError"}
        )

        assert result.success is False
        assert "error" in result.outputs


class TestBackendType:
    """Test BackendType enum"""

    def test_backend_type_values(self):
        """Test backend type enum values"""
        assert BackendType.CREWAI.value == "crewai"
        assert BackendType.CLAUDE_CODE.value == "claude_code"

    def test_backend_type_comparison(self):
        """Test backend type comparison"""
        assert BackendType.CREWAI != BackendType.CLAUDE_CODE
        assert BackendType.CREWAI == BackendType.CREWAI
