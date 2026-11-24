"""
Day 24 Test Suite: Bounded Pagination, Multi-User Isolation, and N+1 Analysis
Runs without external network or complex dependencies using python -s test_day24.py.
"""

import sys
import unittest
from ariadne import graphql_sync
from database import engine, SessionLocal, init_db
from models import User, Task
from main import schema
from query_tracker import QueryTracker


class TestDay24PaginationAndNPlusOne(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Seed synthetic database once for test class."""
        cls.db = init_db()
        cls.tracker = QueryTracker(engine)

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def _execute_gql(self, query: str, variables: dict = None, token: str = "alice-secret-token"):
        """Helper executing GraphQL queries in a clean session context."""
        session = SessionLocal()
        user = session.query(User).filter(User.token == token).first()
        context = {"db": session, "user": user}
        try:
            return graphql_sync(schema, {"query": query, "variables": variables or {}}, context_value=context)
        finally:
            session.close()

    def test_01_bounded_pagination_limits(self):
        """Verify limit cannot exceed 50 items and negative offset is rejected."""
        # 1. Reject limit > 50
        query = """
        query BoundedList($limit: Int) {
            tasks(limit: $limit) {
                total
                limit
                items { id }
            }
        }
        """
        success, response = self._execute_gql(query, {"limit": 100})
        self.assertIsNotNone(response.get("errors"))
        self.assertIn("exceeds maximum allowed page size of 50", response["errors"][0]["message"])

        # 2. Reject negative offset
        neg_query = """
        query NegativeOffset {
            tasks(limit: 10, offset: -5) { total }
        }
        """
        success, neg_response = self._execute_gql(neg_query)
        self.assertIsNotNone(neg_response.get("errors"))
        self.assertIn("Offset must be greater than or equal to 0", neg_response["errors"][0]["message"])

    def test_02_pagination_page_slicing(self):
        """Verify limit and offset slice pages correctly with stable total count."""
        query = """
        query PaginatedTasks($limit: Int, $offset: Int) {
            tasks(limit: $limit, offset: $offset) {
                total
                limit
                offset
                items {
                    id
                    title
                }
            }
        }
        """
        # Page 1: 10 items
        _, resp1 = self._execute_gql(query, {"limit": 10, "offset": 0})
        data1 = resp1["data"]["tasks"]
        self.assertEqual(data1["total"], 30)  # Alice owns 30 tasks
        self.assertEqual(len(data1["items"]), 10)
        first_page_ids = [t["id"] for t in data1["items"]]

        # Page 2: next 10 items
        _, resp2 = self._execute_gql(query, {"limit": 10, "offset": 10})
        data2 = resp2["data"]["tasks"]
        self.assertEqual(data2["total"], 30)
        self.assertEqual(len(data2["items"]), 10)
        second_page_ids = [t["id"] for t in data2["items"]]

        # Ensure no overlap between pages
        self.assertTrue(set(first_page_ids).isdisjoint(set(second_page_ids)))

    def test_03_multi_user_privacy_isolation(self):
        """Verify User Bob cannot access Alice's tasks or see Alice's tasks in list."""
        query = """
        query BobList {
            tasks(limit: 50) {
                total
                items {
                    id
                    ownerId
                }
            }
        }
        """
        # Bob executes tasks query
        _, bob_resp = self._execute_gql(query, token="bob-secret-token")
        bob_tasks = bob_resp["data"]["tasks"]
        self.assertEqual(bob_tasks["total"], 10)  # Bob only owns 10 tasks
        self.assertEqual(len(bob_tasks["items"]), 10)
        for t in bob_tasks["items"]:
            self.assertEqual(t["ownerId"], "2")  # Bob's ID is 2

        # Bob attempts direct read on Alice's task (ID 1)
        task_query = """
        query ReadAliceTask {
            task(id: "1") {
                id
                title
            }
        }
        """
        _, direct_resp = self._execute_gql(task_query, token="bob-secret-token")
        # Missing/forbidden task reads must return null as per Guide Page 5 contract
        self.assertIsNone(direct_resp["data"]["task"])

    def test_04_n_plus_one_query_investigation(self):
        """
        Demonstrates N+1 query detection.
        When fetching N tasks with their nested 'project', unbatched resolution
        executes 1 query for tasks + N individual queries for each project.
        """
        query_with_nested_project = """
        query NestedProjects {
            tasks(limit: 5) {
                items {
                    id
                    title
                    project {
                        id
                        name
                    }
                }
            }
        }
        """
        session = SessionLocal()
        user = session.query(User).filter(User.token == "alice-secret-token").first()
        context = {"db": session, "user": user}

        try:
            with self.tracker.capture():
                graphql_sync(schema, {"query": query_with_nested_project}, context_value=context)

            # Query Count = 1 (SELECT count) + 1 (SELECT tasks) + 5 (individual project SELECTs) = 7 queries
            # Proving that each item triggers an individual query: N+1
            query_count = self.tracker.count
            self.assertGreaterEqual(query_count, 5, f"Expected N+1 queries, got {query_count}")
            print(f"\n[N+1 Investigation] Fetched 5 tasks with nested projects. Emitted {query_count} SQL statements.")
        finally:
            session.close()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDay24PaginationAndNPlusOne)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
