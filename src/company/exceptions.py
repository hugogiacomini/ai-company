"""
Custom exceptions for AI Company simulation.
Provides a hierarchy of exceptions for better error handling.
"""


class AICompanyError(Exception):
    """Base exception for all AI Company errors"""
    pass


class BackendError(AICompanyError):
    """Base exception for backend-related errors"""
    pass


class BackendInitializationError(BackendError):
    """Raised when backend fails to initialize"""
    pass


class BackendNotAvailableError(BackendError):
    """Raised when requested backend is not available"""
    pass


class AgentCreationError(BackendError):
    """Raised when agent creation fails"""
    pass


class TaskCreationError(BackendError):
    """Raised when task creation fails"""
    pass


class WorkflowExecutionError(AICompanyError):
    """Raised when workflow execution fails"""
    pass


class ConfigurationError(AICompanyError):
    """Raised when configuration is invalid"""
    pass


class ValidationError(AICompanyError):
    """Raised when validation fails"""
    pass


class SubagentNotFoundError(AICompanyError):
    """Raised when a subagent file is not found"""
    pass


class DependencyError(AICompanyError):
    """Raised when required dependencies are missing"""
    pass
