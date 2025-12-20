"""
Result caching for AI Company workflows.
Reduces redundant LLM calls by caching workflow results.
"""
import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime, timedelta

from .logging_config import get_logger

logger = get_logger(__name__)


class WorkflowCache:
    """
    Cache for workflow results to reduce redundant LLM calls.

    Features:
    - Hash-based key generation from workflow parameters
    - Configurable TTL (time-to-live)
    - Disk-based persistence
    - Automatic cache invalidation
    """

    def __init__(
        self,
        cache_dir: str = ".cache/workflows",
        ttl_seconds: int = 3600,  # 1 hour default
        enabled: bool = True
    ):
        """
        Initialize the workflow cache.

        Args:
            cache_dir: Directory to store cache files
            ttl_seconds: Cache entry time-to-live in seconds
            enabled: Whether caching is enabled
        """
        self.cache_dir = Path(cache_dir)
        self.ttl_seconds = ttl_seconds
        self.enabled = enabled

        if self.enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Workflow cache initialized: {self.cache_dir} (TTL: {ttl_seconds}s)")
        else:
            logger.info("Workflow cache disabled")

    def _generate_cache_key(
        self,
        department: str,
        backend: str,
        params: Dict[str, Any]
    ) -> str:
        """
        Generate a unique cache key from workflow parameters.

        Args:
            department: Department name
            backend: Backend type (crewai or claude_code)
            params: Workflow parameters

        Returns:
            MD5 hash string as cache key
        """
        # Create a deterministic string representation
        key_data = {
            'department': department,
            'backend': backend,
            'params': params
        }

        # Sort keys for consistent hashing
        key_string = json.dumps(key_data, sort_keys=True)

        # Generate hash
        cache_key = hashlib.md5(key_string.encode()).hexdigest()

        return cache_key

    def _get_cache_file_path(self, cache_key: str) -> Path:
        """Get the file path for a cache key"""
        return self.cache_dir / f"{cache_key}.json"

    def _is_cache_valid(self, cache_file: Path) -> bool:
        """
        Check if a cache file is still valid based on TTL.

        Args:
            cache_file: Path to cache file

        Returns:
            True if cache is still valid, False otherwise
        """
        if not cache_file.exists():
            return False

        # Check file modification time
        file_mtime = cache_file.stat().st_mtime
        current_time = time.time()

        age_seconds = current_time - file_mtime

        is_valid = age_seconds < self.ttl_seconds

        if not is_valid:
            logger.debug(f"Cache expired: {cache_file.name} (age: {age_seconds:.0f}s)")

        return is_valid

    def get(
        self,
        department: str,
        backend: str,
        params: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a cached workflow result.

        Args:
            department: Department name
            backend: Backend type
            params: Workflow parameters

        Returns:
            Cached result dictionary or None if not found/expired
        """
        if not self.enabled:
            return None

        cache_key = self._generate_cache_key(department, backend, params)
        cache_file = self._get_cache_file_path(cache_key)

        if not self._is_cache_valid(cache_file):
            return None

        try:
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)

            logger.info(f"Cache hit: {department} workflow (key: {cache_key[:8]}...)")

            return cached_data.get('result')

        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to read cache file {cache_file}: {e}")
            # Remove corrupted cache file
            cache_file.unlink(missing_ok=True)
            return None

    def set(
        self,
        department: str,
        backend: str,
        params: Dict[str, Any],
        result: Dict[str, Any]
    ) -> None:
        """
        Store a workflow result in the cache.

        Args:
            department: Department name
            backend: Backend type
            params: Workflow parameters
            result: Workflow result to cache
        """
        if not self.enabled:
            return

        cache_key = self._generate_cache_key(department, backend, params)
        cache_file = self._get_cache_file_path(cache_key)

        try:
            cache_data = {
                'department': department,
                'backend': backend,
                'params': params,
                'result': result,
                'cached_at': datetime.now().isoformat(),
                'ttl_seconds': self.ttl_seconds
            }

            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)

            logger.info(f"Cache stored: {department} workflow (key: {cache_key[:8]}...)")

        except (IOError, TypeError) as e:
            logger.warning(f"Failed to write cache file {cache_file}: {e}")

    def invalidate(
        self,
        department: Optional[str] = None,
        backend: Optional[str] = None
    ) -> int:
        """
        Invalidate cached results.

        Args:
            department: If specified, invalidate only this department's cache
            backend: If specified, invalidate only this backend's cache

        Returns:
            Number of cache entries invalidated
        """
        if not self.enabled:
            return 0

        invalidated_count = 0

        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)

                should_invalidate = True

                if department and cache_data.get('department') != department:
                    should_invalidate = False

                if backend and cache_data.get('backend') != backend:
                    should_invalidate = False

                if should_invalidate:
                    cache_file.unlink()
                    invalidated_count += 1
                    logger.debug(f"Invalidated cache: {cache_file.name}")

            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to read cache file {cache_file}: {e}")
                # Remove corrupted file
                cache_file.unlink(missing_ok=True)
                invalidated_count += 1

        logger.info(f"Invalidated {invalidated_count} cache entries")

        return invalidated_count

    def clear_all(self) -> int:
        """
        Clear all cache entries.

        Returns:
            Number of cache entries cleared
        """
        return self.invalidate()

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        if not self.enabled:
            return {
                'enabled': False,
                'total_entries': 0,
                'valid_entries': 0,
                'expired_entries': 0,
                'cache_dir': str(self.cache_dir)
            }

        total_entries = 0
        valid_entries = 0
        expired_entries = 0

        for cache_file in self.cache_dir.glob("*.json"):
            total_entries += 1
            if self._is_cache_valid(cache_file):
                valid_entries += 1
            else:
                expired_entries += 1

        return {
            'enabled': True,
            'total_entries': total_entries,
            'valid_entries': valid_entries,
            'expired_entries': expired_entries,
            'ttl_seconds': self.ttl_seconds,
            'cache_dir': str(self.cache_dir)
        }
