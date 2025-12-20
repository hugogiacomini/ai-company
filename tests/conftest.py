"""Pytest configuration and fixtures"""
import pytest
import os
from pathlib import Path


@pytest.fixture(scope="session")
def test_data_dir():
    """Get test data directory"""
    return Path(__file__).parent / "test_data"


@pytest.fixture(scope="function")
def temp_env_vars(monkeypatch):
    """Fixture to temporarily set environment variables"""
    def _set_env(**kwargs):
        for key, value in kwargs.items():
            monkeypatch.setenv(key, value)
    return _set_env


@pytest.fixture(scope="function")
def mock_openai_key(monkeypatch):
    """Mock OpenAI API key"""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-123")


@pytest.fixture(scope="function")
def clean_cache():
    """Clean cache directory after test"""
    yield
    cache_dir = Path(".cache")
    if cache_dir.exists():
        import shutil
        shutil.rmtree(cache_dir)


@pytest.fixture
def sample_agent_role():
    """Sample agent role for testing"""
    from src.company.backends.base import AgentRole
    return AgentRole(
        role="Test Agent",
        goal="Complete test tasks",
        backstory="Experienced test agent",
        department="test",
        level="expert",
        can_delegate=False,
        skills=["testing", "analysis"]
    )


@pytest.fixture
def sample_task_definition():
    """Sample task definition for testing"""
    from src.company.backends.base import TaskDefinition
    return TaskDefinition(
        description="Test task description",
        agent_role="Test Agent",
        expected_output="Test output format"
    )
