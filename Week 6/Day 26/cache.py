"""
Day 26 Local TTL Cache Fixture & Key Design
Provides an owner-partitioned, thread-safe in-memory cache with deterministic TTL expiration.
Serves as the local contract-compatible replacement for Redis when external labs are offline.
"""

import time
from typing import Any, Optional, Dict, Tuple


class LocalTTLCache:
    """
    In-memory key-value cache with millisecond-precision Time-To-Live (TTL).
    Implements standard get/set/delete/expire semantics matching Redis commands.
    """
    def __init__(self):
        # Internal dictionary: key -> (value, expiry_timestamp)
        self._store: Dict[str, Tuple[Any, float]] = {}

    def set(self, key: str, value: Any, ttl_seconds: float) -> None:
        """Stores value with explicit TTL expiration boundary."""
        expiry = time.time() + ttl_seconds
        self._store[key] = (value, expiry)

    def get(self, key: str) -> Optional[Any]:
        """Retrieves value if not expired; automatically purges stale keys."""
        if key not in self._store:
            return None
        value, expiry = self._store[key]
        if time.time() > expiry:
            # Stale key: purge and return None
            del self._store[key]
            return None
        return value

    def delete(self, key: str) -> bool:
        """Removes key from cache."""
        if key in self._store:
            del self._store[key]
            return True
        return False

    def clear(self) -> None:
        """Flushes all keys."""
        self._store.clear()

    def exists(self, key: str) -> bool:
        """Returns True if key exists and has not expired."""
        return self.get(key) is not None
