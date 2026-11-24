"""
GraphQL Resolvers for Day 23
Delegates all business actions to ItemService and catches DomainError to return safe GraphQL error responses.
"""

from typing import Any, Dict
from ariadne import QueryType, MutationType, EnumType
from graphql import GraphQLError

from services.item_service import ItemService
from domain.exceptions import DomainError, DomainValidationError, DomainPermissionError, DomainNotFoundError

query = QueryType()
mutation = MutationType()

# Bind TaskStatus enum
task_status_enum = EnumType(
    "TaskStatus",
    {
        "OPEN": "OPEN",
        "IN_PROGRESS": "IN_PROGRESS",
        "DONE": "DONE",
    }
)


@query.field("item")
def resolve_item(_: Any, info: Any, id: str) -> Dict[str, Any]:
    """Resolves a single item, enforcing ownership through user context."""
    user_id = info.context.get("user_id")
    try:
        item = ItemService.get_item(id, user_id)
        return {
            "id": item["id"],
            "title": item["title"],
            "status": item["state"],
            "ownerId": item["owner_id"],
        }
    except (DomainNotFoundError, DomainPermissionError):
        # As per Guide Page 5: missing/forbidden task reads return null in GraphQL
        return None


@mutation.field("createTask")
def resolve_create_task(_: Any, info: Any, input: Dict[str, Any]) -> Dict[str, Any]:
    """Creates a task using the shared ItemService."""
    user_id = info.context.get("user_id")
    try:
        item = ItemService.create_item(
            title=input["title"],
            state=input.get("status", "OPEN"),
            owner_id=user_id,
        )
        return {
            "id": item["id"],
            "title": item["title"],
            "status": item["state"],
            "ownerId": item["owner_id"],
        }
    except DomainError as exc:
        raise GraphQLError(str(exc))


@mutation.field("updateTask")
def resolve_update_task(_: Any, info: Any, id: str, input: Dict[str, Any]) -> Dict[str, Any]:
    """Updates task title/status while respecting ownership and state transition rules."""
    user_id = info.context.get("user_id")
    try:
        item = ItemService.update_item(
            item_id=id,
            title=input.get("title"),
            state=input.get("status"),
            requesting_user_id=user_id,
        )
        return {
            "id": item["id"],
            "title": item["title"],
            "status": item["state"],
            "ownerId": item["owner_id"],
        }
    except DomainError as exc:
        raise GraphQLError(str(exc))


@mutation.field("deleteTask")
def resolve_delete_task(_: Any, info: Any, id: str) -> Dict[str, Any]:
    """Deletes task through shared ItemService."""
    user_id = info.context.get("user_id")
    try:
        result = ItemService.delete_item(item_id=id, requesting_user_id=user_id)
        return result
    except DomainError as exc:
        raise GraphQLError(str(exc))


bindables = [query, mutation, task_status_enum]
