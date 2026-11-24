"""
Day 23 Verification Suite
Validates business rule parity between REST transport and GraphQL resolvers:
1. Title validation (<5 chars rejected).
2. Status state transitions (illegal jumps like OPEN -> DONE rejected).
3. Cross-user modification rejection (User B cannot update/delete User A's task).
"""

import sys
import unittest
from ariadne import graphql_sync
from main import schema, ItemService
from domain.exceptions import DomainValidationError, DomainPermissionError, DomainNotFoundError


class TestDay23Parity(unittest.TestCase):
    def setUp(self):
        """Reset in-memory storage before each test."""
        ItemService.clear_all()

    def test_01_valid_creation_rest_and_graphql(self):
        """Test valid task creation via service layer and GraphQL mutation."""
        # 1. Via Service (REST backing)
        rest_task = ItemService.create_item("Implement Ariadne Resolvers", "OPEN", "alice")
        self.assertEqual(rest_task["title"], "Implement Ariadne Resolvers")
        self.assertEqual(rest_task["state"], "OPEN")
        self.assertEqual(rest_task["owner_id"], "alice")

        # 2. Via GraphQL Mutation
        mutation = """
        mutation Create($input: TaskInput!) {
            createTask(input: $input) {
                id
                title
                status
                ownerId
            }
        }
        """
        variables = {"input": {"title": "Implement GraphQL Parity Checks", "status": "OPEN"}}
        success, response = graphql_sync(schema, {"query": mutation, "variables": variables}, context_value={"user_id": "alice"})
        self.assertTrue(success)
        self.assertIsNone(response.get("errors"))
        gql_task = response["data"]["createTask"]
        self.assertEqual(gql_task["title"], "Implement GraphQL Parity Checks")
        self.assertEqual(gql_task["status"], "OPEN")
        self.assertEqual(gql_task["ownerId"], "alice")

    def test_02_invalid_short_title_rejected_by_both(self):
        """Verify title < 5 characters is rejected with DomainValidationError in both layers."""
        # 1. Service Layer rejection (REST returns 400)
        with self.assertRaises(DomainValidationError):
            ItemService.create_item("abc", "OPEN", "alice")

        # 2. GraphQL Mutation rejection
        mutation = """
        mutation Create($input: TaskInput!) {
            createTask(input: $input) { id }
        }
        """
        variables = {"input": {"title": "abc", "status": "OPEN"}}
        success, response = graphql_sync(schema, {"query": mutation, "variables": variables}, context_value={"user_id": "alice"})
        self.assertIsNotNone(response.get("errors"))
        self.assertIn("Title must be between 5 and 80 characters", response["errors"][0]["message"])

    def test_03_invalid_state_transition_rejected_by_both(self):
        """
        Verify illegal status transition (OPEN -> DONE) is rejected.
        Allowed: OPEN -> IN_PROGRESS, IN_PROGRESS -> OPEN/DONE, DONE -> IN_PROGRESS.
        """
        task = ItemService.create_item("Draft Sprint Deliverables", "OPEN", "alice")

        # 1. REST Layer update rejection
        with self.assertRaises(DomainValidationError):
            ItemService.update_item(task["id"], title=None, state="DONE", requesting_user_id="alice")

        # 2. GraphQL Mutation update rejection
        mutation = """
        mutation Update($id: ID!, $input: TaskUpdate!) {
            updateTask(id: $id, input: $input) { id status }
        }
        """
        variables = {"id": task["id"], "input": {"status": "DONE"}}
        success, response = graphql_sync(schema, {"query": mutation, "variables": variables}, context_value={"user_id": "alice"})
        self.assertIsNotNone(response.get("errors"))
        self.assertIn("Invalid status transition from OPEN to DONE", response["errors"][0]["message"])

    def test_04_cross_user_modification_rejected_by_both(self):
        """Verify User B cannot update or delete User A's task (DomainPermissionError)."""
        task = ItemService.create_item("Confidential Project Strategy", "OPEN", "alice")

        # 1. User B attempts update via Service Layer (REST returns 403)
        with self.assertRaises(DomainPermissionError):
            ItemService.update_item(task["id"], title="Hacked Title", state=None, requesting_user_id="bob")

        # 2. User B attempts mutation via GraphQL
        mutation = """
        mutation Update($id: ID!, $input: TaskUpdate!) {
            updateTask(id: $id, input: $input) { id }
        }
        """
        variables = {"id": task["id"], "input": {"title": "Hacked Title via GraphQL"}}
        success, response = graphql_sync(schema, {"query": mutation, "variables": variables}, context_value={"user_id": "bob"})
        self.assertIsNotNone(response.get("errors"))
        self.assertIn("Access denied", response["errors"][0]["message"])

        # 3. User B attempts delete via GraphQL
        delete_mutation = """
        mutation Delete($id: ID!) {
            deleteTask(id: $id) { id deleted }
        }
        """
        success, del_response = graphql_sync(schema, {"query": delete_mutation, "variables": {"id": task["id"]}}, context_value={"user_id": "bob"})
        self.assertIsNotNone(del_response.get("errors"))
        self.assertIn("Access denied", del_response["errors"][0]["message"])

        # 4. Verify owner record was NOT modified
        original = ItemService.get_item(task["id"], "alice")
        self.assertEqual(original["title"], "Confidential Project Strategy")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDay23Parity)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
