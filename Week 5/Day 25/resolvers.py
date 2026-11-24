"""
Day 25 Ariadne GraphQL Resolvers
Implements the shared contract queries and mutations.
Contains an acceptance check switch `INJECT_RESOLVER_DEFECT` to demonstrate that a deliberate defect makes tests fail.
"""

from typing import Any, Dict, Optional
from ariadne import QueryType, MutationType, EnumType
from graphql import GraphQLError
from sqlalchemy.orm import Session
from models import User, Task, PriorityEnum, TaskStatusEnum
from service import TaskService, TaskDomainError, TaskValidationError, TaskPermissionError

# Flag for acceptance check: setting this to True simulates a broken resolver
INJECT_RESOLVER_DEFECT = False

query = QueryType()
mutation = MutationType()

priority_enum = EnumType(
    "Priority",
    {
        "LOW": "LOW",
        "NORMAL": "NORMAL",
        "HIGH": "HIGH",
    }
)

task_status_enum = EnumType(
    "TaskStatus",
    {
        "OPEN": "OPEN",
        "IN_PROGRESS": "IN_PROGRESS",
        "DONE": "DONE",
    }
)


# --- Query Resolvers ---

@query.field("me")
def resolve_me(_: Any, info: Any) -> Dict[str, Any]:
    """Returns the authenticated user info."""
    user: Optional[User] = info.context.get("user")
    if not user:
        raise GraphQLError("Unauthenticated: Valid Bearer token required.")
    return {
        "id": str(user.id),
        "email": user.email,
    }


@query.field("tasks")
def resolve_tasks(_: Any, info: Any, limit: int = 20, offset: int = 0, status: Optional[str] = None) -> Dict[str, Any]:
    """Returns bounded paginated list of tasks for the authenticated user."""
    user: Optional[User] = info.context.get("user")
    if not user:
        raise GraphQLError("Unauthenticated.")

    # Deliberate Defect Injection for Acceptance Check
    if INJECT_RESOLVER_DEFECT:
        # Broken resolver: leaks all users' tasks or ignores ownership!
        effective_owner_id = 9999
    else:
        effective_owner_id = user.id

    db: Session = info.context.get("db")
    try:
        items, total = TaskService.list_tasks(
            db=db,
            owner_id=effective_owner_id,
            limit=limit,
            offset=offset,
            status_str=status
        )
        return {
            "items": [
                {
                    "id": str(t.id),
                    "title": t.title,
                    "priority": t.priority.value,
                    "status": t.status.value,
                    "ownerId": str(t.owner_id),
                }
                for t in items
            ],
            "total": total,
        }
    except TaskDomainError as exc:
        raise GraphQLError(str(exc))


@query.field("task")
def resolve_task(_: Any, info: Any, id: str) -> Optional[Dict[str, Any]]:
    """Resolves single task. Missing or forbidden tasks return null as per contract."""
    user: Optional[User] = info.context.get("user")
    if not user:
        raise GraphQLError("Unauthenticated.")

    db: Session = info.context.get("db")
    try:
        task_id = int(id)
    except ValueError:
        return None

    task = TaskService.get_task(db=db, owner_id=user.id, task_id=task_id)
    if not task:
        return None

    return {
        "id": str(task.id),
        "title": task.title,
        "priority": task.priority.value,
        "status": task.status.value,
        "ownerId": str(task.owner_id),
    }


# --- Mutation Resolvers ---

@mutation.field("createTask")
def resolve_create_task(_: Any, info: Any, input: Dict[str, Any]) -> Dict[str, Any]:
    """Creates task after trimming title and setting priority."""
    user: Optional[User] = info.context.get("user")
    if not user:
        raise GraphQLError("Unauthenticated.")

    db: Session = info.context.get("db")
    try:
        task = TaskService.create_task(
            db=db,
            owner_id=user.id,
            title=input["title"],
            priority_str=input.get("priority", "NORMAL")
        )
        return {
            "id": str(task.id),
            "title": task.title,
            "priority": task.priority.value,
            "status": task.status.value,
            "ownerId": str(task.owner_id),
        }
    except TaskDomainError as exc:
        raise GraphQLError(str(exc))


@mutation.field("updateTask")
def resolve_update_task(_: Any, info: Any, id: str, input: Dict[str, Any]) -> Dict[str, Any]:
    """Updates task fields enforcing ownership and valid status transitions."""
    user: Optional[User] = info.context.get("user")
    if not user:
        raise GraphQLError("Unauthenticated.")

    db: Session = info.context.get("db")
    try:
        task_id = int(id)
        task = TaskService.update_task(
            db=db,
            owner_id=user.id,
            task_id=task_id,
            title=input.get("title"),
            priority_str=input.get("priority"),
            status_str=input.get("status")
        )
        return {
            "id": str(task.id),
            "title": task.title,
            "priority": task.priority.value,
            "status": task.status.value,
            "ownerId": str(task.owner_id),
        }
    except TaskDomainError as exc:
        raise GraphQLError(str(exc))


@mutation.field("deleteTask")
def resolve_delete_task(_: Any, info: Any, id: str) -> Dict[str, Any]:
    """Deletes task if owned by user."""
    user: Optional[User] = info.context.get("user")
    if not user:
        raise GraphQLError("Unauthenticated.")

    db: Session = info.context.get("db")
    try:
        task_id = int(id)
        deleted = TaskService.delete_task(db=db, owner_id=user.id, task_id=task_id)
        return {"id": id, "deleted": deleted}
    except TaskDomainError as exc:
        raise GraphQLError(str(exc))


bindables = [query, mutation, priority_enum, task_status_enum]
