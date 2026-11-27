"""
Day 28 Local Job Queue Fixture & Durability Demonstration
Simulates an in-process background worker (like FastAPI BackgroundTasks)
and demonstrates its fundamental limitation: volatile state lost on process crash.
"""

from typing import Dict, Optional, Callable
import uuid
from job_models import JobStatus, JobRecord


class LocalJobQueue:
    """
    In-memory job executor.
    Shows the durability limits of same-process background tasks:
    if the worker crashes before a job finishes, pending and running jobs are permanently lost.
    """
    def __init__(self):
        self.jobs: Dict[str, JobRecord] = {}

    def enqueue(self, owner_id: int, task_name: str) -> JobRecord:
        """Enqueues a job into PENDING state."""
        job_id = f"job-{uuid.uuid4().hex[:8]}"
        record = JobRecord(job_id=job_id, owner_id=owner_id, task_name=task_name)
        self.jobs[job_id] = record
        return record

    def process_job(self, job_id: str, work_func: Callable[[], dict]) -> JobRecord:
        """Executes the job, transitioning through RUNNING to SUCCESS or FAILED."""
        record = self.jobs.get(job_id)
        if not record:
            raise ValueError(f"Job {job_id} not found.")

        record.mark_running()
        try:
            output = work_func()
            record.mark_success(output)
        except Exception as exc:
            record.mark_failed(str(exc))
        return record

    def simulate_process_crash(self) -> int:
        """
        Simulates an unexpected process termination (SIGKILL / power loss).
        All in-memory jobs are lost!
        Returns the number of jobs lost.
        """
        lost_count = len(self.jobs)
        self.jobs.clear()
        return lost_count
