"""
Day 26 Dependency Timeout Configuration
Defines strict, bounded timeout budgets for critical and external dependencies.
Prevents thread/connection pool exhaustion caused by cascading service hangs.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DependencyTimeouts:
    """Bounded timeout configuration (in seconds)."""
    # Database connection pool checkout timeout
    DB_POOL_TIMEOUT_SECONDS: float = 3.0

    # Individual SQL query statement timeout
    DB_QUERY_TIMEOUT_SECONDS: float = 2.0

    # Cache read/write operation timeout (Redis or local fixture)
    CACHE_OP_TIMEOUT_SECONDS: float = 0.5

    # Outbound HTTP/External dependency timeout
    EXTERNAL_API_TIMEOUT_SECONDS: float = 2.5

    # Short default TTL for volatile task list caches
    TASK_CACHE_TTL_SECONDS: float = 2.0


CONFIG = DependencyTimeouts()
