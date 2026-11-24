"""
Day 25 Task Service Layer
Enforces domain rules consistently across REST and GraphQL:
- Title length: 5-80 chars trimmed
- State transitions:
  * OPEN -> IN_PROGRESS
  * IN_PROGRESS -> OPEN or DONE
  * DONE -> IN_PROGRESS
- Ownership verification: Users can only view, update, or delete their own tasks.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from models import Task, PriorityEnum, TaskStatusEnum

ALLOWED_TRANSITIONS = {
    TaskStatusEnum.OPEN: {TaskStatusEnum.IN_PROGRESS},
    TaskStatusEnum.IN_PROGRESS: {TaskStatusEnum.OPEN, TaskStatusEnum.DONE},
    TaskStatusEnum.DONE: {TaskStatusEnum.IN_PROGRESS},
}


class TaskDomainError(Exception):
    """Base domain exception."""
    pass


class TaskValidationError(TaskDomainError):
    """Raised on invalid titles or illegal status transitions."""
    pass


class TaskPermissionError(TaskDomainError):
    """Raised when an operation violates ownership boundaries."""
    pass


class TaskService:
    @staticmethod
    def validate_title(title: str) -> str:
        """Trims whitespace and checks 5-80 character constraint."""
        if not title:
            raise TaskValidationError("Title must not be empty.")
        trimmed = title.strip()
        if len(trimmed) < 5 or len(trimmed) > 80:
            raise TaskValidationError(f"Title must be between 5 and 80 characters. Got {len(trimmed)}.")
        return trimmed

    @staticmethod
    def validate_status_transition(current: TaskStatusEnum, target: TaskStatusEnum) -> None:
        """Enforces allowed state machine transitions."""
        if current == target:
            return
        allowed = ALLOWED_TRANSITIONS.get(current, set())
        if target not in allowed:
            allowed_names = [s.value for s in allowed]
            raise TaskValidationError(
                f"Invalid status transition from {current.value} to {target.value}. Allowed: {allowed_names}"
            )

    @classmethod
    def create_task(cls, db: Session, owner_id: int, title: str, priority_str: str = "NORMAL") -> Task:
        """Creates a new owned task."""
        trimmed = cls.validate_title(title)
        priority = PriorityEnum(priority_str.upper())
        task = Task(title=trimmed, priority=priority, status=TaskStatusEnum.OPEN, owner_id=owner_id)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @classmethod
    def get_task(cls, db: Session, owner_id: int, task_id: int) -> Optional[Task]:
        """Retrieves task enforcing ownership (returns None if not owned or not found)."""
        return db.query(Task).filter(Task.id == task_id, Task.owner_id == owner_id).first()

    @classmethod
    def list_tasks(cls, db: Session, owner_id: int, limit: int = 20, offset: int = 0, status_str: Optional[str] = None):
        """Lists tasks for owner with bounded pagination (1-50 items)."""
        if limit < 1 or limit > 50:
            raise TaskValidationError(f"Limit must be between 1 and 50. Got {limit}.")
        if offset < 0:
            raise TaskValidationError(f"Offset must be non-negative. Got {offset}.")

        query = db.query(Task).filter(Task.owner_id == owner_id)
        if status_str:
            status_enum = TaskStatusEnum(status_str.upper())
            query = query.filter(Task.status == status_enum)

        total = query.count()
        items = query.order_by(Task.id.asc()).offset(offset).limit(limit).all()
        return items, total

    @classmethod
    def update_task(cls, db: Session, owner_id: int, task_id: int, title: Optional[str] = None, priority_str: Optional[str] = None, status_str: Optional[str] = None) -> Task:
        """Updates task enforcing ownership and valid transitions."""
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise TaskValidationError(f"Task with ID {task_id} not found.")
        if task.owner_id != owner_id:
            raise TaskPermissionError(f"Permission denied: Task {task_id} belongs to another user.")

        if title is not None:
            task.title = cls.validate_title(title)

        if priority_str is not None:
            task.priority = PriorityEnum(priority_str.upper())

        if status_str is not None:
            target_status = TaskStatusEnum(status_str.upper())
            cls.validate_status_transition(task.status, target_status)
            task.status = target_status

        db.commit()
        db.refresh(task)
        return task

    @classmethod
    def delete_task(cls, db: Session, owner_id: int, task_id: int) -> bool:
        """Deletes task if owned by user."""
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise TaskValidationError(f"Task with ID {task_id} not found.")
        if task.owner_id != owner_id:
            raise TaskPermissionError(f"Permission denied: Task {task_id} belongs to another user.")

        db.delete(task)
        db.commit()
        return True
