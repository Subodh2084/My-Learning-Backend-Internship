"""
ItemService - Core Business Logic Service
Ensures business rules are identical across both REST and GraphQL APIs:
1. Title validation: 5-80 trimmed characters.
2. Status state transitions:
   - OPEN -> IN_PROGRESS
   - IN_PROGRESS -> OPEN or DONE
   - DONE -> IN_PROGRESS
3. Resource ownership: users cannot modify or delete tasks owned by another user.
"""

from typing import Dict, Any, Optional
import uuid
from domain.exceptions import DomainValidationError, DomainPermissionError, DomainNotFoundError

# In-memory storage for Day 23 demonstration
# In production, this interfaces with SQLAlchemy repository
_ITEMS_STORE: Dict[str, Dict[str, Any]] = {}

# Allowed status transitions as per Course Guide Page 5 Shared Contract
ALLOWED_TRANSITIONS = {
    "OPEN": {"IN_PROGRESS"},
    "IN_PROGRESS": {"OPEN", "DONE"},
    "DONE": {"IN_PROGRESS"},
}


class ItemService:
    """
    Service enforcing domain rules without any knowledge of HTTP, ASGI, or GraphQL.
    Both REST endpoints and GraphQL resolvers delegate directly to this class.
    """

    @staticmethod
    def _validate_title(title: str) -> str:
        """Trims and validates title length between 5 and 80 characters."""
        if not title:
            raise DomainValidationError("Title must not be empty.")
        trimmed = title.strip()
        if len(trimmed) < 5 or len(trimmed) > 80:
            raise DomainValidationError(
                f"Title must be between 5 and 80 characters. Received length: {len(trimmed)}"
            )
        return trimmed

    @staticmethod
    def _validate_status_transition(current_status: str, new_status: str) -> None:
        """Validates that status transition follows state-machine rules."""
        current = current_status.upper()
        target = new_status.upper()
        if target not in {"OPEN", "IN_PROGRESS", "DONE"}:
            raise DomainValidationError(f"Invalid status: '{new_status}'. Allowed: OPEN, IN_PROGRESS, DONE.")
        if target == current:
            return  # No state change
        allowed = ALLOWED_TRANSITIONS.get(current, set())
        if target not in allowed:
            raise DomainValidationError(
                f"Invalid status transition from {current} to {target}. Allowed: {sorted(list(allowed))}"
            )

    @classmethod
    def create_item(cls, title: str, state: str, owner_id: str) -> Dict[str, Any]:
        """Creates a new item after validating title and initializing state."""
        trimmed_title = cls._validate_title(title)
        initial_state = state.upper() if state else "OPEN"
        if initial_state not in {"OPEN", "IN_PROGRESS", "DONE"}:
            raise DomainValidationError(f"Invalid initial state: '{state}'. Allowed: OPEN, IN_PROGRESS, DONE.")

        item_id = str(uuid.uuid4())[:8]
        new_item = {
            "id": item_id,
            "title": trimmed_title,
            "state": initial_state,
            "owner_id": owner_id,
        }
        _ITEMS_STORE[item_id] = new_item
        return new_item

    @classmethod
    def get_item(cls, item_id: str, requesting_user_id: str) -> Dict[str, Any]:
        """Retrieves item enforcing ownership privacy."""
        item = _ITEMS_STORE.get(item_id)
        if not item:
            raise DomainNotFoundError(f"Item with id '{item_id}' not found.")
        if item["owner_id"] != requesting_user_id:
            raise DomainPermissionError("Access denied: You do not own this item.")
        return item

    @classmethod
    def update_item(
        cls,
        item_id: str,
        title: Optional[str],
        state: Optional[str],
        requesting_user_id: str
    ) -> Dict[str, Any]:
        """Updates item fields while validating title length, state transition, and ownership."""
        item = cls.get_item(item_id, requesting_user_id)

        if title is not None:
            item["title"] = cls._validate_title(title)

        if state is not None:
            cls._validate_status_transition(item["state"], state)
            item["state"] = state.upper()

        return item

    @classmethod
    def delete_item(cls, item_id: str, requesting_user_id: str) -> Dict[str, Any]:
        """Deletes item after verifying ownership."""
        item = cls.get_item(item_id, requesting_user_id)
        del _ITEMS_STORE[item_id]
        return {"id": item_id, "deleted": True}

    @classmethod
    def clear_all(cls) -> None:
        """Utility for test isolation."""
        _ITEMS_STORE.clear()
