"""
Day 26 Verification Suite: Dependency Timeouts and TTL Cache Expiry
Checks:
1. Bounded timeout limits are enforced.
2. Owner-partitioned keys prevent cross-user data leakage.
3. Cache entries expire deterministically at the exact TTL boundary.
"""

import sys
import time
import unittest
from config import CONFIG
from cache import LocalTTLCache
from service import CachedTaskService


class TestDay26CacheAndTimeouts(unittest.TestCase):
    def setUp(self):
        self.cache = LocalTTLCache()
        self.service = CachedTaskService(self.cache)

    def test_01_timeout_budgets_are_bounded(self):
        """Verify timeout configurations are bounded and strictly positive."""
        self.assertLessEqual(CONFIG.DB_POOL_TIMEOUT_SECONDS, 5.0)
        self.assertLessEqual(CONFIG.DB_QUERY_TIMEOUT_SECONDS, 3.0)
        self.assertLessEqual(CONFIG.CACHE_OP_TIMEOUT_SECONDS, 1.0)
        self.assertGreater(CONFIG.TASK_CACHE_TTL_SECONDS, 0.0)

    def test_02_owner_key_isolation(self):
        """Verify Alice and Bob have distinct cache keys preventing leakage."""
        alice_key = self.service.build_cache_key(owner_id=1, offset=0, limit=10)
        bob_key = self.service.build_cache_key(owner_id=2, offset=0, limit=10)

        self.assertNotEqual(alice_key, bob_key)
        self.assertEqual(alice_key, "user:1:tasks:page:0:10")
        self.assertEqual(bob_key, "user:2:tasks:page:0:10")

        # Read for Alice and Bob
        alice_data = self.service.get_tasks_page(owner_id=1, offset=0, limit=10)
        bob_data = self.service.get_tasks_page(owner_id=2, offset=0, limit=10)

        self.assertEqual(self.cache.get(alice_key)[0]["title"], "Alice Task 1")
        self.assertEqual(self.cache.get(bob_key)[0]["title"], "Bob Task 1")

    def test_03_ttl_expiration_at_boundary(self):
        """Verify cache entry expires at the documented TTL boundary."""
        short_key = "user:1:tasks:page:0:5"
        # Set short TTL of 0.2 seconds
        self.cache.set(short_key, [{"id": 1}], ttl_seconds=0.2)

        # Immediate read succeeds
        self.assertTrue(self.cache.exists(short_key))
        self.assertIsNotNone(self.cache.get(short_key))

        # Sleep past TTL boundary (0.25 seconds)
        time.sleep(0.25)

        # Read after TTL expires returns None
        self.assertFalse(self.cache.exists(short_key))
        self.assertIsNone(self.cache.get(short_key))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDay26CacheAndTimeouts)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
