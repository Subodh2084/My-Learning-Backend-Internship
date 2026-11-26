"""
Day 27 Verification Suite: Read Consistency After Writes
Proves:
1. Omitting cache invalidation causes stale reads (acceptance scenario).
2. Active cache invalidation guarantees read-after-write consistency across create, update, and delete.
"""

import sys
import unittest
from cache_service import CacheAsideTaskService


class TestDay27ReadConsistency(unittest.TestCase):
    def setUp(self):
        self.service = CacheAsideTaskService()
        # Seed initial task
        self.service.create_task(task_id=1, title="Initial Task", owner_id=1)

    def test_01_stale_read_demonstration_without_invalidation(self):
        """
        Acceptance Scenario:
        Demonstrate that without invalidation, a read following a write returns stale cached data.
        """
        # Step 1: Initial read populates the cache
        initial_list = self.service.list_tasks(owner_id=1)
        self.assertEqual(len(initial_list), 1)

        # Step 2: Disable invalidation to reproduce stale behavior
        self.service.ENABLE_WRITE_INVALIDATION = False

        # Step 3: Perform write (create second task in DB)
        self.service.create_task(task_id=2, title="Second Task", owner_id=1)

        # Step 4: Subsequent read returns stale cache (still length 1, missing Task 2)
        stale_list = self.service.list_tasks(owner_id=1)
        self.assertEqual(len(stale_list), 1, "Stale cache returned old record count!")
        self.assertEqual(stale_list[0]["id"], 1)

    def test_02_read_after_write_consistency_with_invalidation(self):
        """
        Guarantees that with write-invalidation enabled, reads immediately reflect creates, updates, and deletes.
        """
        self.service.ENABLE_WRITE_INVALIDATION = True

        # 1. Warm cache
        self.assertEqual(len(self.service.list_tasks(owner_id=1)), 1)

        # 2. Write: Create Task 2
        self.service.create_task(task_id=2, title="Fresh Task 2", owner_id=1)

        # Readback immediately shows 2 items
        fresh_list = self.service.list_tasks(owner_id=1)
        self.assertEqual(len(fresh_list), 2)
        self.assertEqual(fresh_list[1]["title"], "Fresh Task 2")

        # 3. Update Task 1 status to IN_PROGRESS
        self.service.update_task_status(task_id=1, new_status="IN_PROGRESS", owner_id=1)
        updated_list = self.service.list_tasks(owner_id=1)
        task_1 = next(t for t in updated_list if t["id"] == 1)
        self.assertEqual(task_1["status"], "IN_PROGRESS")

        # 4. Delete Task 2
        self.service.delete_task(task_id=2, owner_id=1)
        after_delete_list = self.service.list_tasks(owner_id=1)
        self.assertEqual(len(after_delete_list), 1)
        self.assertEqual(after_delete_list[0]["id"], 1)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDay27ReadConsistency)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
