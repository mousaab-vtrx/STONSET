"""
Standard API response wrapper.
All endpoints return this format.
"""
from typing import Any, Optional
from fastapi.responses import JSONResponse


class ApiResponse:
    """Standard API response envelope."""

    def __init__(
        self,
        status: str = "success",
        data: Optional[Any] = None,
        message: str = "",
        code: Optional[str] = None,
        errors: Optional[dict[str, Any]] = None,
        meta: Optional[dict[str, Any]] = None,
    ):
        """Initialize response."""
        self.status = status
        self.data = data
        self.message = message
        self.code = code
        self.errors = errors
        self.meta = meta

    def dict(self) -> dict[str, Any]:
        """Convert to dict."""
        return {
            "status": self.status,
            "data": self.data,
            "message": self.message,
            "code": self.code,
            "errors": self.errors,
            "meta": self.meta,
        }


def success_response(
    data: Optional[Any] = None,
    message: str = "Success",
    meta: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Create success response."""
    return ApiResponse(
        status="success",
        data=data,
        message=message,
        meta=meta,
    ).dict()


def error_response(
    message: str = "Error",
    code: str = "ERROR",
    errors: Optional[dict[str, Any]] = None,
    status_code: int = 400,
) -> JSONResponse:
    """Create error response with proper HTTP status."""
    return JSONResponse(
        status_code=status_code,
        content=ApiResponse(
            status="error",
            message=message,
            code=code,
            errors=errors,
        ).dict(),
    )
