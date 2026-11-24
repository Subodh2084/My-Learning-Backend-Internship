# Domain-level exception hierarchy for TaskFlow application.
# These exceptions are raised by core business services, independent of the transport layer (REST or GraphQL).

class DomainError(Exception):
    """Base exception for all domain-specific errors."""
    pass


class DomainValidationError(DomainError):
    """
    Raised when an input violates business rules.
    Examples: title length not within 5-80 chars, invalid status transitions.
    Maps to HTTP 400 Bad Request in REST and user error in GraphQL.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class DomainPermissionError(DomainError):
    """
    Raised when an authenticated user attempts to access or mutate a resource owned by someone else.
    Maps to HTTP 403 Forbidden in REST and authorization error in GraphQL.
    """
    def __init__(self, message: str = "Permission denied: resource owned by another user."):
        super().__init__(message)
        self.message = message


class DomainNotFoundError(DomainError):
    """
    Raised when a requested resource does not exist.
    Maps to HTTP 404 Not Found in REST and null / not-found error in GraphQL.
    """
    def __init__(self, message: str = "Resource not found."):
        super().__init__(message)
        self.message = message
