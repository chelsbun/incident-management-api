"""
API Response envelope schemas.

Provides standardized response format for all API endpoints following
WorkFlow Rule 8: consistent response structure with success/data/error/message.

Author: Project
Last Modified: 2026-02-12
"""
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response envelope."""

    success: bool = Field(description="Whether the request succeeded")
    data: T | None = Field(default=None, description="Response data on success")
    error: str | None = Field(default=None, description="Error message on failure")
    message: str = Field(description="Human-readable message")


def success_response(data: T, message: str = "Success") -> ApiResponse[T]:
    """Helper to create success response."""
    return ApiResponse(success=True, data=data, error=None, message=message)


def error_response(error: str, message: str = "Request failed") -> ApiResponse[None]:
    """Helper to create error response."""
    return ApiResponse(success=False, data=None, error=error, message=message)
