"""
Day 25 Test Suite: GraphQL Practical Review
Covers:
1. Queries (me, tasks, task)
2. Mutations (createTask, updateTask, deleteTask)
3. Invalid operation diagnostics (inspecting 'errors' payload, not HTTP 200)
4. Multi-user ownership checks
5. Acceptance Check: Confirms that injecting a deliberate resolver defect causes tests to fail.
"""

import sys
import unittest
from ariadne import graphql_sync
from database import engine, SessionLocal, init_db
from models import User, Task
from main import schema
import resolvers


class TestDay25GraphQLReview(unittest.TestCase):
    def setUp(self):
        """Re-seed database before each test for fresh isolation."""
        init_db()
        resolvers.INJECT_RESOLVER_DEFECT = False

    def _execute(self, query: str, variables: dict = None, token: str = "token-alice-secret"):
        session = SessionLocal()
        user = session.query(User).filter(User.token == token).first() if token else None
        context = {"db": session, "user": user}
        try:
            return graphql_sync(schema, {"query": query, "variables": variables or {}}, context_value=context)
        finally:
            session.close()

    def test_01_query_me_authenticated(self):
        """Query current authenticated user."""
        query = "query { me { id email } }"
        success, response = self._execute(query, token="token-alice-secret")
        self.assertTrue(success)
        self.assertIsNone(response.get("errors"))
        self.assertEqual(response["data"]["me"]["email"], "alice@taskflow.dev")

    def test_02_query_me_unauthenticated_returns_error(self):
        """Unauthenticated requests return a structured GraphQL error."""
        query = "query { me { id email } }"
        success, response = self._execute(query, token=None)
        self.assertIsNotNone(response.get("errors"))
        self.assertIn("Unauthenticated", response["errors"][0]["message"])

    def test_03_create_task_mutation(self):
        """Create a task with title trimming and default priority."""
        mutation = """
        mutation Create($input: TaskInput!) {
            createTask(input: $input) {
                id
                title
                priority
                status
                ownerId
            }
        }
        """
        variables = {"input": {"title": "  Implement GraphQL CI pipeline   ", "priority": "HIGH"}}
        success, response = self._execute(mutation, variables=variables, token="token-alice-secret")
        self.assertTrue(success)
        self.assertIsNone(response.get("errors"))
        task_data = response["data"]["createTask"]
        self.assertEqual(task_data["title"], "Implement GraphQL CI pipeline")  # Verified trimmed
        self.assertEqual(task_data["priority"], "HIGH")
        self.assertEqual(task_data["status"], "OPEN")
        self.assertEqual(task_data["ownerId"], "1")

    def test_04_invalid_title_length_diagnosed(self):
        """Short title (< 5 characters) yields diagnosable error in 'errors' array."""
        mutation = """
        mutation Create($input: TaskInput!) {
            createTask(input: $input) { id }
        }
        """
        variables = {"input": {"title": "xyz"}}
        success, response = self._execute(mutation, variables=variables, token="token-alice-secret")
        self.assertIsNotNone(response.get("errors"))
        self.assertIn("Title must be between 5 and 80 characters", response["errors"][0]["message"])

    def test_05_status_transition_rules(self):
        """Verify allowed and disallowed state transitions."""
        # Task 1 starts IN_PROGRESS. Transitioning to DONE is allowed.
        mutation = """
        mutation Update($id: ID!, $input: TaskUpdate!) {
            updateTask(id: $id, input: $input) { id status }
        }
        """
        success, response = self._execute(mutation, {"id": "1", "input": {"status": "DONE"}}, token="token-alice-secret")
        self.assertIsNone(response.get("errors"))
        self.assertEqual(response["data"]["updateTask"]["status"], "DONE")

        # Transitioning DONE to OPEN directly is illegal (must go to IN_PROGRESS first)
        fail_success, fail_resp = self._execute(mutation, {"id": "1", "input": {"status": "OPEN"}}, token="token-alice-secret")
        self.assertIsNotNone(fail_resp.get("errors"))
        self.assertIn("Invalid status transition from DONE to OPEN", fail_resp["errors"][0]["message"])

    def test_06_two_user_ownership_isolation(self):
        """User Bob cannot update or delete Alice's task."""
        mutation = """
        mutation UpdateAliceTask($id: ID!, $input: TaskUpdate!) {
            updateTask(id: $id, input: $input) { id }
        }
        """
        success, response = self._execute(mutation, {"id": "1", "input": {"title": "Bob Attack"}}, token="token-bob-secret")
        self.assertIsNotNone(response.get("errors"))
        self.assertIn("Permission denied", response["errors"][0]["message"])

    def test_07_deliberate_resolver_defect_acceptance_check(self):
        """
        Acceptance Check Requirement:
        'A deliberate resolver defect makes a meaningful check fail.'
        When INJECT_RESOLVER_DEFECT is True, Alice's task listing is corrupted,
        and this check proves that our verification detects the defect immediately!
        """
        query = "query { tasks { total items { id } } }"

        # 1. Normal state: Alice sees her 2 initial tasks
        resolvers.INJECT_RESOLVER_DEFECT = False
        _, normal_resp = self._execute(query, token="token-alice-secret")
        self.assertEqual(normal_resp["data"]["tasks"]["total"], 2)

        # 2. Defect state: resolver is intentionally broken
        resolvers.INJECT_RESOLVER_DEFECT = True
        _, defect_resp = self._execute(query, token="token-alice-secret")
        # Defect returns 0 tasks for fake owner 9999 instead of Alice's 2 tasks
        corrupted_total = defect_resp["data"]["tasks"]["total"]
        self.assertNotEqual(corrupted_total, 2, "Defect should cause a mismatch!")
        self.assertEqual(corrupted_total, 0, "Corrupted resolver returned unexpected result.")
        resolvers.INJECT_RESOLVER_DEFECT = False


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDay25GraphQLReview)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
