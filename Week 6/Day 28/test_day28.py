"""
Day 28 Verification Suite: Job Lifecycle States and Durability Limits
Checks:
1. Valid job transitions: PENDING -> RUNNING -> SUCCESS.
2. Failure handling: PENDING -> RUNNING -> FAILED with recorded error message.
3. Process crash simulation proves in-memory jobs are lost (durability boundary).
"""

import sys
import unittest
from job_models import JobStatus
from job_queue import LocalJobQueue


class TestDay28JobStates(unittest.TestCase):
    def setUp(self):
        self.queue = LocalJobQueue()

    def test_01_successful_job_lifecycle(self):
        """Verify normal transition: PENDING -> RUNNING -> SUCCESS."""
        job = self.queue.enqueue(owner_id=1, task_name="generate_monthly_csv")
        self.assertEqual(job.status, JobStatus.PENDING)
        self.assertIsNone(job.result)

        # Execute successful work
        def dummy_report():
            return {"rows_exported": 150, "format": "CSV"}

        completed_job = self.queue.process_job(job.job_id, dummy_report)
        self.assertEqual(completed_job.status, JobStatus.SUCCESS)
        self.assertEqual(completed_job.result["rows_exported"], 150)
        self.assertIsNotNone(completed_job.completed_at)

    def test_02_failed_job_captures_error(self):
        """Verify failing job transitions to FAILED and stores error string."""
        job = self.queue.enqueue(owner_id=2, task_name="export_corrupted_data")

        def faulty_work():
            raise RuntimeError("Database connection timed out during streaming")

        failed_job = self.queue.process_job(job.job_id, faulty_work)
        self.assertEqual(failed_job.status, JobStatus.FAILED)
        self.assertIn("connection timed out", failed_job.error)
        self.assertIsNone(failed_job.result)

    def test_03_durability_limit_demonstrated_on_crash(self):
        """
        Acceptance Check:
        Explain and demonstrate what is lost when the in-process worker stops.
        In-memory jobs are wiped on process restart, proving the need for external queues (ARQ/Redis).
        """
        self.queue.enqueue(owner_id=1, task_name="pending_job_1")
        self.queue.enqueue(owner_id=1, task_name="pending_job_2")
        self.assertEqual(len(self.queue.jobs), 2)

        # Simulate process crash
        lost = self.queue.simulate_process_crash()
        self.assertEqual(lost, 2)
        self.assertEqual(len(self.queue.jobs), 0, "In-process memory lost all unexecuted jobs on restart!")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDay28JobStates)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
