"""
Day 27 Cache-Aside Service with Write Invalidation
Demonstrates read-after-write consistency:
When a task is created, updated, or deleted, all corresponding cache entries for the owner are purged,
preventing stale reads on the subsequent request.
"""

from typing import Dict, List, Any, Optional
import time


class CacheAsideTaskService:
    """
    Manages task persistence with cache-aside read caching and active write invalidation.
    Supports a toggle `ENABLE_WRITE_INVALIDATION` to demonstrate stale read behavior when invalidation is omitted.
    """
    def __init__(self):
        # Database table simulation
        self.database: Dict[int, Dict[str, Any]] = {}
        # Local TTL Cache simulation: key -> (value, expiry)
        self.cache: Dict[str, Any] = {}
        # Invalidation control flag (for demonstration and acceptance testing)
        self.ENABLE_WRITE_INVALIDATION: bool = True

    def _get_owner_pattern(self, owner_id: int) -> str:
        return f"user:{owner_id}:tasks"

    def invalidate_owner_cache(self, owner_id: int) -> None:
        """Purges all cached pages belonging to this user."""
        prefix = self._get_owner_pattern(owner_id)
        keys_to_delete = [k for k in self.cache.keys() if k.startswith(prefix)]
        for k in keys_to_delete:
            del self.cache[k]

    def list_tasks(self, owner_id: int) -> List[Dict[str, Any]]:
        """Read-through cache: return cached copy if available, otherwise query DB."""
        cache_key = f"user:{owner_id}:tasks:all"
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Query DB
        tasks = [t for t in self.database.values() if t["owner_id"] == owner_id]
        # Store in cache
        self.cache[cache_key] = tasks.copy()
        return tasks

    def create_task(self, task_id: int, title: str, owner_id: int) -> Dict[str, Any]:
        """Creates task in DB and conditionally invalidates user cache."""
        task = {"id": task_id, "title": title, "owner_id": owner_id, "status": "OPEN"}
        self.database[task_id] = task

        if self.ENABLE_WRITE_INVALIDATION:
            self.invalidate_owner_cache(owner_id)

        return task

    def update_task_status(self, task_id: int, new_status: str, owner_id: int) -> Dict[str, Any]:
        """Updates task in DB and conditionally invalidates user cache."""
        task = self.database.get(task_id)
        if not task or task["owner_id"] != owner_id:
            raise ValueError("Task not found or access denied.")

        task["status"] = new_status
        if self.ENABLE_WRITE_INVALIDATION:
            self.invalidate_owner_cache(owner_id)

        return task

    def delete_task(self, task_id: int, owner_id: int) -> bool:
        """Deletes task in DB and conditionally invalidates user cache."""
        task = self.database.get(task_id)
        if not task or task["owner_id"] != owner_id:
            raise ValueError("Task not found or access denied.")

        del self.database[task_id]
        if self.ENABLE_WRITE_INVALIDATION:
            self.invalidate_owner_cache(owner_id)

        return True
