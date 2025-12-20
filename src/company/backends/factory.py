"""
Backend factory for creating and initializing backends.
Handles backend selection based on configuration.
"""
from typing import Optional, Dict, Any

from .base import BaseBackend, BackendType
from .crewai_backend import CrewAIBackend
from ..config.config_loader import ConfigLoader
from ..exceptions import BackendError, BackendNotAvailableError, ConfigurationError


class BackendFactory:
    """Factory for creating and configuring backends"""

    @staticmethod
    def create_backend(
        backend_type: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> BaseBackend:
        """
        Create and initialize a backend.

        Args:
            backend_type: Backend to create ('crewai' or 'claude_code').
                         If None, reads from config or environment.
            config: Configuration dictionary. If None, loads from default location.

        Returns:
            Initialized backend instance

        Raises:
            ValueError: If backend_type is invalid or backend not available
        """
        # Load config if not provided
        if config is None:
            config = ConfigLoader.load_config()

        # Determine backend type
        if backend_type is None:
            backend_type = config.get('backend', 'crewai')

        # Normalize backend type
        backend_type = backend_type.lower()

        # Create appropriate backend
        if backend_type == BackendType.CREWAI.value:
            backend = CrewAIBackend()
            backend_config = ConfigLoader.get_backend_config('crewai', config)
        elif backend_type == BackendType.CLAUDE_CODE.value:
            # Import here to avoid circular dependency
            try:
                from .claude_code_backend import ClaudeCodeBackend
                backend = ClaudeCodeBackend()
                backend_config = ConfigLoader.get_backend_config('claude_code', config)
            except ImportError as e:
                raise BackendNotAvailableError(
                    f"Claude Code backend not available: {e}. "
                    f"Ensure all dependencies are installed."
                ) from e
        else:
            raise ConfigurationError(
                f"Unknown backend type: '{backend_type}'. "
                f"Valid options are: {[bt.value for bt in BackendType]}"
            )

        # Initialize backend with config
        backend.initialize(backend_config)

        return backend

    @staticmethod
    def get_available_backends() -> list[str]:
        """
        Get list of available backend types.

        Returns:
            List of backend type strings
        """
        return [bt.value for bt in BackendType]

    @staticmethod
    def is_backend_available(backend_type: str) -> bool:
        """
        Check if a backend is available.

        Args:
            backend_type: Backend type to check

        Returns:
            True if backend is available, False otherwise
        """
        backend_type = backend_type.lower()

        if backend_type == BackendType.CREWAI.value:
            try:
                import crewai
                return True
            except ImportError:
                return False
        elif backend_type == BackendType.CLAUDE_CODE.value:
            try:
                from .claude_code_backend import ClaudeCodeBackend
                return True
            except ImportError:
                return False
        else:
            return False
