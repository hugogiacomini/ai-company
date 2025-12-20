"""Tests for CrewAI backend implementation"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.company.backends.crewai_backend import CrewAIBackend
from src.company.backends.base import AgentRole, TaskDefinition, BackendType


class TestCrewAIBackend:
    """Test CrewAI backend implementation"""

    @pytest.fixture
    def backend(self):
        """Create a CrewAI backend instance"""
        backend = CrewAIBackend()
        backend.initialize({'verbose': False})
        return backend

    def test_initialization(self, backend):
        """Test backend initialization"""
        assert backend.get_backend_type() == BackendType.CREWAI
        assert backend._config == {'verbose': False}

    def test_create_agent(self, backend):
        """Test agent creation"""
        agent_def = AgentRole(
            role="Test Agent",
            goal="Test goal",
            backstory="Test backstory",
            department="test",
            level="expert",
            can_delegate=False,
            skills=["skill1"]
        )

        with patch('src.company.backends.crewai_backend.Agent') as mock_agent:
            mock_agent.return_value = MagicMock()
            agent = backend.create_agent(agent_def)

            mock_agent.assert_called_once()
            call_kwargs = mock_agent.call_args[1]
            assert call_kwargs['role'] == "Test Agent"
            assert call_kwargs['goal'] == "Test goal"
            assert call_kwargs['allow_delegation'] is False
            assert call_kwargs['max_iter'] == 3

    def test_create_agent_with_delegation(self, backend):
        """Test creating an agent that can delegate"""
        agent_def = AgentRole(
            role="CEO",
            goal="Lead company",
            backstory="Experienced leader",
            department="executive",
            level="executive",
            can_delegate=True,
            skills=["leadership"]
        )

        with patch('src.company.backends.crewai_backend.Agent') as mock_agent:
            mock_agent.return_value = MagicMock()
            agent = backend.create_agent(agent_def)

            call_kwargs = mock_agent.call_args[1]
            assert call_kwargs['allow_delegation'] is True
            assert call_kwargs['max_iter'] == 5

    def test_create_task(self, backend):
        """Test task creation"""
        # First create an agent
        agent_def = AgentRole(
            role="Test Agent",
            goal="Test",
            backstory="Test",
            department="test",
            level="expert",
            can_delegate=False,
            skills=[]
        )

        with patch('src.company.backends.crewai_backend.Agent') as mock_agent:
            mock_agent_instance = MagicMock()
            mock_agent.return_value = mock_agent_instance
            backend.create_agent(agent_def)

            # Now create a task
            task_def = TaskDefinition(
                description="Test task",
                agent_role="Test Agent",
                expected_output="Test output"
            )

            with patch('src.company.backends.crewai_backend.Task') as mock_task:
                mock_task.return_value = MagicMock()
                task = backend.create_task(task_def)

                mock_task.assert_called_once()
                call_kwargs = mock_task.call_args[1]
                assert call_kwargs['description'] == "Test task"
                assert call_kwargs['expected_output'] == "Test output"
                assert call_kwargs['agent'] == mock_agent_instance

    def test_create_task_without_agent_fails(self, backend):
        """Test that creating a task without an agent raises error"""
        task_def = TaskDefinition(
            description="Test task",
            agent_role="Nonexistent Agent",
            expected_output="Test output"
        )

        with pytest.raises(ValueError, match="Agent 'Nonexistent Agent' not found"):
            backend.create_task(task_def)

    @patch('src.company.backends.crewai_backend.Crew')
    @patch('src.company.backends.crewai_backend.Agent')
    @patch('src.company.backends.crewai_backend.Task')
    def test_execute_workflow(self, mock_task, mock_agent, mock_crew, backend):
        """Test workflow execution"""
        # Setup mocks
        mock_agent_instance = MagicMock()
        mock_agent.return_value = mock_agent_instance
        mock_task_instance = MagicMock()
        mock_task.return_value = mock_task_instance
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = "Workflow result"
        mock_crew.return_value = mock_crew_instance

        # Create agents and tasks
        agents = [mock_agent_instance]
        tasks = [mock_task_instance]

        # Execute workflow
        result = backend.execute_workflow(agents, tasks, "sequential")

        # Verify
        assert result.success is True
        assert result.outputs["result"] == "Workflow result"
        assert result.metadata["backend"] == "crewai"
        assert result.metadata["agents_count"] == 1
        assert result.metadata["tasks_count"] == 1
        mock_crew_instance.kickoff.assert_called_once()

    def test_supports_parallel_execution(self, backend):
        """Test that CrewAI backend doesn't support parallel execution"""
        assert backend.supports_parallel_execution() is False

    def test_cleanup(self, backend):
        """Test cleanup clears cache"""
        # Add an agent to cache
        agent_def = AgentRole(
            role="Test Agent",
            goal="Test",
            backstory="Test",
            department="test",
            level="expert",
            can_delegate=False,
            skills=[]
        )

        with patch('src.company.backends.crewai_backend.Agent'):
            backend.create_agent(agent_def)
            assert len(backend._agents_cache) > 0

            backend.cleanup()
            assert len(backend._agents_cache) == 0
