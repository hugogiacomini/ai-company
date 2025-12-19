"""
Configuration loader for AI Company.
Loads backend configuration from YAML file and environment variables.
"""
import os
from typing import Dict, Any, Optional
from pathlib import Path
import yaml


class ConfigLoader:
    """Loads and manages configuration from multiple sources"""

    DEFAULT_CONFIG_PATH = "config/company_config.yaml"
    ENV_VAR_BACKEND = "AI_COMPANY_BACKEND"
    ENV_VAR_CONFIG_PATH = "AI_COMPANY_CONFIG_PATH"

    @classmethod
    def load_config(cls, config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Load configuration from YAML file and environment variables.

        Environment variables override YAML configuration.

        Args:
            config_path: Optional path to config file. If None, uses default or env var.

        Returns:
            Dictionary with configuration
        """
        # Determine config file path
        if config_path is None:
            config_path = os.getenv(cls.ENV_VAR_CONFIG_PATH, cls.DEFAULT_CONFIG_PATH)

        # Load config from file
        config = cls._load_yaml_config(config_path)

        # Override with environment variables
        backend_env = os.getenv(cls.ENV_VAR_BACKEND)
        if backend_env:
            config['backend'] = backend_env

        return config

    @classmethod
    def _load_yaml_config(cls, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from YAML file.

        Args:
            config_path: Path to YAML config file

        Returns:
            Dictionary with configuration

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid YAML
        """
        path = Path(config_path)

        if not path.exists():
            # Return default config if file doesn't exist
            return cls._get_default_config()

        try:
            with open(path, 'r') as f:
                config = yaml.safe_load(f)
                return config or cls._get_default_config()
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config file {config_path}: {e}")

    @classmethod
    def _get_default_config(cls) -> Dict[str, Any]:
        """
        Get default configuration.

        Returns:
            Dictionary with default configuration
        """
        return {
            'backend': 'crewai',  # Default to crewai for backward compatibility
            'crewai': {
                'verbose': True,
                'max_iterations': {
                    'executive': 5,
                    'head': 5,
                    'specialist': 3
                }
            },
            'claude_code': {
                'subagents_dir': '.claude/agents',
                'model': 'sonnet',
                'parallel_execution': True,
                'max_parallel_tasks': 5
            },
            'company': {
                'name': 'AI Company Inc.',
                'departments': [
                    'executive',
                    'marketing',
                    'operations',
                    'human_resources',
                    'software_development',
                    'commercial'
                ]
            }
        }

    @classmethod
    def get_backend_config(cls, backend_name: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get configuration for a specific backend.

        Args:
            backend_name: Name of backend ('crewai' or 'claude_code')
            config: Full config dictionary. If None, loads from default location.

        Returns:
            Dictionary with backend-specific configuration
        """
        if config is None:
            config = cls.load_config()

        return config.get(backend_name, {})
