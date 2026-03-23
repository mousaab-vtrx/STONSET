"""
Custom exceptions for the application.
"""


class AppException(Exception):
    """Base application exception with a user-friendly message and code."""

    def __init__(self, message: str, status_code: int = 400, code: str = "ERROR"):
        self.message = message
        self.status_code = status_code
        self.code = code
        super().__init__(self.message)


# Alias for backwards compatibility
ApplicationError = AppException


class NotFoundException(AppException):
    """Resource not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404, code="NOT_FOUND")


# Aliases for backwards compatibility
NotFoundError = NotFoundException


class UnauthorizedException(AppException):
    """User not authenticated."""

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401, code="UNAUTHORIZED")


class ForbiddenException(AppException):
    """User not authorized to perform action."""

    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403, code="FORBIDDEN")


class ValidationException(AppException):
    """Validation error."""

    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status_code=422, code="VALIDATION_ERROR")


class ConflictException(AppException):
    """Resource already exists or conflict."""

    def __init__(self, message: str = "Conflict"):
        super().__init__(message, status_code=409, code="CONFLICT")


class AuthenticationError(AppException):
    """Authentication failed."""

    def __init__(self, message: str = "Authentication failed", status_code: int = 401, code: str = "AUTH_FAILED"):
        super().__init__(message, status_code=status_code, code=code)


class ConflictError(AppException):
    """Resource already exists."""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, status_code=409, code="CONFLICT")
