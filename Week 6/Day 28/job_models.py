"""
Day 28 Job Models & State Machine
Defines the discrete lifecycle states for asynchronous background jobs:
PENDING -> RUNNING -> SUCCESS | FAILED
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import uuid


class JobStatus(str, Enum):
    """Discrete lifecycle states for queued background jobs."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


@dataclass
class JobRecord:
    """Represents a background report job and its execution state."""
    job_id: str
    owner_id: int
    task_name: str
    status: JobStatus = JobStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

    def mark_running(self) -> None:
        self.status = JobStatus.RUNNING

    def mark_success(self, result: Dict[str, Any]) -> None:
        self.status = JobStatus.SUCCESS
        self.result = result
        self.completed_at = datetime.now(timezone.utc)

    def mark_failed(self, error_message: str) -> None:
        self.status = JobStatus.FAILED
        self.error = error_message
        self.completed_at = datetime.now(timezone.utc)
