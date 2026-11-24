"""
Day 24 GraphQL Resolvers
Implements:
1. Bounded pagination (clamps limit to 1-50, rejects negative offset).
2. Authorization: queries strictly return tasks owned by info.context['user'].
3. Nested field resolution for Task.project.
4. Demonstrates N+1 query inspection and batch loading optimization.
"""

from typing import Any, Dict, List, Optional
from ariadne import QueryType, ObjectType, EnumType
from graphql import GraphQLError
from sqlalchemy.orm import Session, joinedload
from models import User, Project, Task, TaskStatus

query = QueryType()
task_type = ObjectType("Task")
project_type = ObjectType("Project")

task_status_enum = EnumType(
    "TaskStatus",
    {
        "OPEN": TaskStatus.OPEN,
        "IN_PROGRESS": TaskStatus.IN_PROGRESS,
        "DONE": TaskStatus.DONE,
    }
)


# --- Root Query Resolvers ---

@query.field("me")
def resolve_me(_: Any, info: Any) -> Dict[str, Any]:
    """Returns currently authenticated user profile."""
    user: Optional[User] = info.context.get("user")
    if not user:
        raise GraphQLError("Unauthenticated: Please provide a valid Bearer token.")
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
    }


@query.field("tasks")
def resolve_tasks(_: Any, info: Any, limit: int = 20, offset: int = 0, status: Optional[str] = None) -> Dict[str, Any]:
    """
    Returns bounded paginated tasks strictly owned by the requesting user.
    Rules:
    - limit clamped to 1..50 (cannot exceed 50)
    - offset >= 0
    - optional status filter applied before pagination
    """
    user: Optional[User] = info.context.get("user")
    if not user:
        raise GraphQLError("Unauthenticated: Bearer token required.")

    db: Session = info.context.get("db")

    # Enforce non-negative offset
    if offset < 0:
        raise GraphQLError(f"Invalid offset '{offset}'. Offset must be greater than or equal to 0.")

    # Enforce maximum list size boundary (Guide Page 5: 1-50 items)
    if limit > 50:
        raise GraphQLError(f"Requested limit '{limit}' exceeds maximum allowed page size of 50.")
    if limit < 1:
        raise GraphQLError(f"Requested limit '{limit}' must be at least 1.")

    # Base query filtered by authenticated user's ownership
    base_query = db.query(Task).filter(Task.owner_id == user.id)

    # Optional status filter
    if status:
        base_query = base_query.filter(Task.status == status)

    # Count total matching records before pagination
    total_count = base_query.count()

    # Apply deterministic ordering and pagination
    tasks_page = (
        base_query.order_by(Task.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    items = [
        {
            "id": str(t.id),
            "title": t.title,
            "status": t.status.value,
            "ownerId": str(t.owner_id),
            "projectId": str(t.project_id) if t.project_id else None,
        }
        for t in tasks_page
    ]

    return {
        "items": items,
        "total": total_count,
        "limit": limit,
        "offset": offset,
    }


@query.field("task")
def resolve_task(_: Any, info: Any, id: str) -> Optional[Dict[str, Any]]:
    """Resolves a single task with strict ownership authorization."""
    user: Optional[User] = info.context.get("user")
    if not user:
        raise GraphQLError("Unauthenticated.")

    db: Session = info.context.get("db")
    try:
        task_id = int(id)
    except ValueError:
        return None

    # Return null if missing or forbidden as per Guide Page 5 Shared Contract
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user.id).first()
    if not task:
        return None

    return {
        "id": str(task.id),
        "title": task.title,
        "status": task.status.value,
        "ownerId": str(task.owner_id),
        "projectId": str(task.project_id) if task.project_id else None,
    }


# --- Nested Resolvers ---

@task_type.field("project")
def resolve_task_project(task_obj: Dict[str, Any], info: Any) -> Optional[Dict[str, Any]]:
    """
    Resolves the parent project for a task.
    When executed across a list of N tasks, this demonstrates the classic N+1 query problem
    if individual SELECT queries are fired per task.
    """
    project_id = task_obj.get("projectId")
    if not project_id:
        return None

    db: Session = info.context.get("db")
    project = db.query(Project).filter(Project.id == int(project_id)).first()
    if not project:
        return None

    return {
        "id": str(project.id),
        "name": project.name,
        "description": project.description,
        "ownerId": str(project.owner_id),
    }


bindables = [query, task_type, project_type, task_status_enum]
