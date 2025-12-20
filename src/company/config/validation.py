"""
Configuration validation for AI Company.
Validates configuration files and environment variables.
"""
import os
from typing import Dict, Any, List, Optional
from ..exceptions import ConfigurationError, ValidationError
from ..backends.base import BackendType
from ..utils.logging_config import get_logger

logger = get_logger(__name__)


class ConfigValidator:
    """
    Validates AI Company configuration.

    Performs validation on:
    - Backend selection and availability
    - Environment variables (API keys)
    - Cache configuration
    - Department and company settings
    """

    REQUIRED_FIELDS = {
        'backend': str,
        'company': dict,
        'cache': dict
    }

    BACKEND_REQUIREMENTS = {
        BackendType.CREWAI.value: {
            'env_vars': ['OPENAI_API_KEY'],
            'config_fields': ['verbose']
        },
        BackendType.CLAUDE_CODE.value: {
            'env_vars': [],  # Optional ANTHROPIC_API_KEY
            'config_fields': ['subagents_dir', 'model']
        }
    }

    @classmethod
    def validate_config(cls, config: Dict[str, Any]) -> None:
        """
        Validate complete configuration.

        Args:
            config: Configuration dictionary

        Raises:
            ConfigurationError: If configuration is invalid
            ValidationError: If specific validation fails
        """
        try:
            cls._validate_structure(config)
            cls._validate_backend(config)
            cls._validate_cache_config(config)
            cls._validate_company_config(config)
            logger.info("Configuration validation successful")
        except (ConfigurationError, ValidationError) as e:
            logger.error(f"Configuration validation failed: {e}")
            raise

    @classmethod
    def _validate_structure(cls, config: Dict[str, Any]) -> None:
        """
        Validate basic configuration structure.

        Args:
            config: Configuration dictionary

        Raises:
            ConfigurationError: If required fields are missing or have wrong type
        """
        errors = []

        for field, expected_type in cls.REQUIRED_FIELDS.items():
            if field not in config:
                errors.append(f"Missing required field: '{field}'")
            elif not isinstance(config[field], expected_type):
                errors.append(
                    f"Field '{field}' must be of type {expected_type.__name__}, "
                    f"got {type(config[field]).__name__}"
                )

        if errors:
            raise ConfigurationError(
                f"Invalid configuration structure:\n  - " + "\n  - ".join(errors)
            )

    @classmethod
    def _validate_backend(cls, config: Dict[str, Any]) -> None:
        """
        Validate backend configuration and requirements.

        Args:
            config: Configuration dictionary

        Raises:
            ConfigurationError: If backend is invalid or requirements not met
        """
        backend = config.get('backend')

        # Check if backend is valid
        valid_backends = [b.value for b in BackendType]
        if backend not in valid_backends:
            raise ConfigurationError(
                f"Invalid backend: '{backend}'. "
                f"Must be one of: {', '.join(valid_backends)}"
            )

        # Check backend-specific requirements
        requirements = cls.BACKEND_REQUIREMENTS.get(backend, {})

        # Validate environment variables
        missing_env_vars = []
        for env_var in requirements.get('env_vars', []):
            if not os.getenv(env_var):
                missing_env_vars.append(env_var)

        if missing_env_vars:
            raise ConfigurationError(
                f"Backend '{backend}' requires the following environment variables:\n"
                f"  - " + "\n  - ".join(missing_env_vars) + "\n"
                f"Please set them in your .env file or environment."
            )

        # Validate backend config section exists
        if backend not in config:
            raise ConfigurationError(
                f"Missing configuration section for backend '{backend}'"
            )

        # Validate required config fields for backend
        backend_config = config[backend]
        missing_fields = []
        for field in requirements.get('config_fields', []):
            if field not in backend_config:
                missing_fields.append(field)

        if missing_fields:
            raise ConfigurationError(
                f"Backend '{backend}' configuration missing required fields:\n"
                f"  - " + "\n  - ".join(missing_fields)
            )

        logger.debug(f"Backend '{backend}' validation successful")

    @classmethod
    def _validate_cache_config(cls, config: Dict[str, Any]) -> None:
        """
        Validate cache configuration.

        Args:
            config: Configuration dictionary

        Raises:
            ValidationError: If cache configuration is invalid
        """
        cache_config = config.get('cache', {})

        errors = []

        # Validate enabled field
        if 'enabled' in cache_config:
            if not isinstance(cache_config['enabled'], bool):
                errors.append("cache.enabled must be a boolean (true/false)")

        # Validate cache_dir field
        if 'cache_dir' in cache_config:
            cache_dir = cache_config['cache_dir']
            if not isinstance(cache_dir, str):
                errors.append("cache.cache_dir must be a string")
            elif not cache_dir.strip():
                errors.append("cache.cache_dir cannot be empty")

        # Validate ttl_seconds field
        if 'ttl_seconds' in cache_config:
            ttl = cache_config['ttl_seconds']
            if not isinstance(ttl, int):
                errors.append("cache.ttl_seconds must be an integer")
            elif ttl < 0:
                errors.append("cache.ttl_seconds must be non-negative")
            elif ttl > 86400:  # 24 hours
                logger.warning(
                    f"cache.ttl_seconds is very large ({ttl}s = {ttl/3600:.1f} hours). "
                    "Consider a smaller value to avoid stale cache."
                )

        if errors:
            raise ValidationError(
                f"Invalid cache configuration:\n  - " + "\n  - ".join(errors)
            )

        logger.debug("Cache configuration validation successful")

    @classmethod
    def _validate_company_config(cls, config: Dict[str, Any]) -> None:
        """
        Validate company configuration.

        Args:
            config: Configuration dictionary

        Raises:
            ValidationError: If company configuration is invalid
        """
        company_config = config.get('company', {})

        errors = []

        # Validate company name
        if 'name' in company_config:
            name = company_config['name']
            if not isinstance(name, str):
                errors.append("company.name must be a string")
            elif not name.strip():
                errors.append("company.name cannot be empty")

        # Validate departments
        if 'departments' in company_config:
            departments = company_config['departments']
            if not isinstance(departments, list):
                errors.append("company.departments must be a list")
            elif not departments:
                errors.append("company.departments cannot be empty")
            else:
                # Check for valid department names
                valid_departments = [
                    'executive', 'marketing', 'operations',
                    'human_resources', 'software_development', 'commercial'
                ]
                for dept in departments:
                    if dept not in valid_departments:
                        errors.append(
                            f"Invalid department '{dept}'. "
                            f"Valid: {', '.join(valid_departments)}"
                        )

        if errors:
            raise ValidationError(
                f"Invalid company configuration:\n  - " + "\n  - ".join(errors)
            )

        logger.debug("Company configuration validation successful")

    @classmethod
    def validate_environment(cls, backend: Optional[str] = None) -> None:
        """
        Validate environment variables for a specific backend.

        Args:
            backend: Backend type to validate (if None, validates all)

        Raises:
            ConfigurationError: If required environment variables are missing
        """
        if backend:
            backends_to_check = [backend]
        else:
            backends_to_check = [b.value for b in BackendType]

        all_errors = []

        for backend_type in backends_to_check:
            requirements = cls.BACKEND_REQUIREMENTS.get(backend_type, {})
            missing = []

            for env_var in requirements.get('env_vars', []):
                if not os.getenv(env_var):
                    missing.append(env_var)

            if missing:
                all_errors.append(
                    f"Backend '{backend_type}' missing: {', '.join(missing)}"
                )

        if all_errors:
            raise ConfigurationError(
                "Environment validation failed:\n  - " + "\n  - ".join(all_errors)
            )

        logger.debug("Environment validation successful")

    @classmethod
    def get_validation_summary(cls, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get a summary of configuration validation.

        Args:
            config: Configuration dictionary

        Returns:
            Dictionary with validation summary
        """
        summary = {
            'valid': False,
            'backend': config.get('backend'),
            'errors': [],
            'warnings': []
        }

        try:
            cls.validate_config(config)
            summary['valid'] = True
        except (ConfigurationError, ValidationError) as e:
            summary['errors'].append(str(e))

        # Check for warnings
        cache_config = config.get('cache', {})
        if cache_config.get('enabled') and cache_config.get('ttl_seconds', 0) > 86400:
            summary['warnings'].append(
                "Cache TTL is very large (>24 hours), may lead to stale results"
            )

        backend = config.get('backend')
        if backend == BackendType.CLAUDE_CODE.value and not os.getenv('ANTHROPIC_API_KEY'):
            summary['warnings'].append(
                "ANTHROPIC_API_KEY not set - Claude Code backend may have limited functionality"
            )

        return summary
