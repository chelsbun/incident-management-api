"""
Ticket Pydantic schemas for request/response validation.

Defines input validation and output serialization models for ticket endpoints.
All fields are validated at the API boundary before reaching business logic.

Author: Project
Last Modified: 2026-02-12
"""

from datetime import datetime

from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    """
    Schema for creating a new ticket.

    Validates:
        - Title length (1-200 chars)
        - Priority enum (low, medium, high, urgent)
        - Optional description
    """

    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    priority: str = Field(default="medium", pattern="^(low|medium|high|urgent)$")


class TicketOut(BaseModel):
    """
    Schema for ticket output.

    Returns full ticket details including server-generated fields
    (id, status, created_at).
    """

    id: int
    title: str
    description: str | None
    status: str
    priority: str
    created_at: datetime

    class Config:
        from_attributes = True
