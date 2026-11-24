# Package initializer for domain exceptions
from .exceptions import DomainError, DomainValidationError, DomainPermissionError, DomainNotFoundError

__all__ = ["DomainError", "DomainValidationError", "DomainPermissionError", "DomainNotFoundError"]
