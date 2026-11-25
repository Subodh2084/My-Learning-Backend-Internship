"""
Day 26 Owner-Partitioned Cache Key Strategy
Demonstrates secure key naming to prevent cross-user cache collisions:
Format: user:{owner_id}:tasks:page:{offset}:{limit}
"""

from typing import List, Dict, Any, Optional
from cache import LocalTTLCache
from config import CONFIG


class CachedTaskService:
    """
    Task service wrapper using owner-partitioned cache keys with short TTL.
    """
    def __init__(self, cache: LocalTTLCache):
        self.cache = cache
        # Simulated database store
        self.db_records = {
            1: [{"id": 101, "title": "Alice Task 1", "owner_id": 1}],
            2: [{"id": 201, "title": "Bob Task 1", "owner_id": 2}],
        }

    @staticmethod
    def build_cache_key(owner_id: int, offset: int, limit: int) -> str:
        """
        Constructs an owner-isolated cache key.
        Guarantees that User 2's cache lookup cannot collide with User 1's cache.
        """
        return f"user:{owner_id}:tasks:page:{offset}:{limit}"

    def get_tasks_page(self, owner_id: int, offset: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Cache-aside read:
        1. Check owner-specific cache key.
        2. On cache hit, return cached value immediately.
        3. On cache miss, fetch from database and populate cache with TTL.
        """
        key = self.build_cache_key(owner_id, offset, limit)
        cached = self.cache.get(key)
        if cached is not None:
            return cached

        # Simulated DB read
        records = self.db_records.get(owner_id, [])[offset : offset + limit]
        self.cache.set(key, records, ttl_seconds=CONFIG.TASK_CACHE_TTL_SECONDS)
        return records
