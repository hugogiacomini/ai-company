"""Tests for backend factory"""
import pytest
from unittest.mock import patch, MagicMock
from src.company.backends.factory import BackendFactory
from src.company.backends.base import BackendType
from src.company.backends.crewai_backend import CrewAIBackend


class TestBackendFactory:
    """Test backend factory functionality"""

    def test_create_crewai_backend(self):
        """Test creating CrewAI backend"""
        backend = BackendFactory.create_backend('crewai')
        assert backend.get_backend_type() == BackendType.CREWAI
        assert isinstance(backend, CrewAIBackend)

    def test_create_backend_with_uppercase(self):
        """Test backend creation with uppercase name"""
        backend = BackendFactory.create_backend('CREWAI')
        assert backend.get_backend_type() == BackendType.CREWAI

    def test_create_backend_from_config(self):
        """Test creating backend from config"""
        config = {
            'backend': 'crewai',
            'crewai': {'verbose': False}
        }
        backend = BackendFactory.create_backend(config=config)
        assert backend.get_backend_type() == BackendType.CREWAI

    def test_create_backend_invalid_type(self):
        """Test creating backend with invalid type"""
        with pytest.raises(ValueError, match="Unknown backend type"):
            BackendFactory.create_backend('invalid_backend')

    def test_get_available_backends(self):
        """Test getting list of available backends"""
        backends = BackendFactory.get_available_backends()
        assert 'crewai' in backends
        assert 'claude_code' in backends
        assert len(backends) == 2

    def test_is_backend_available_crewai(self):
        """Test checking if CrewAI backend is available"""
        assert BackendFactory.is_backend_available('crewai') is True

    def test_is_backend_available_invalid(self):
        """Test checking invalid backend availability"""
        assert BackendFactory.is_backend_available('invalid') is False

    @patch.dict('os.environ', {'AI_COMPANY_BACKEND': 'crewai'})
    def test_create_backend_from_env(self):
        """Test creating backend from environment variable"""
        backend = BackendFactory.create_backend()
        assert backend.get_backend_type() == BackendType.CREWAI


class TestClaudeCodeBackendCreation:
    """Test Claude Code backend creation"""

    @patch('src.company.backends.factory.ClaudeCodeBackend')
    def test_create_claude_code_backend(self, mock_claude_backend):
        """Test creating Claude Code backend"""
        mock_instance = MagicMock()
        mock_instance.get_backend_type.return_value = BackendType.CLAUDE_CODE
        mock_claude_backend.return_value = mock_instance

        backend = BackendFactory.create_backend('claude_code')
        mock_claude_backend.assert_called_once()
