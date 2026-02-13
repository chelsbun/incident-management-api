"""
Ticket ORM model.

Defines the database schema for incident tickets using SQLAlchemy 2.0
mapped_column syntax with type hints.

Author: Project
Last Modified: 2026-02-12
"""
from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Ticket(Base):
    """
    Ticket model for incident and issue tracking.

    Attributes:
        id: Primary key
        title: Short description of the ticket (max 200 chars)
        description: Detailed description (optional)
        status: Current status (open, in_progress, resolved, closed)
        priority: Priority level (low, medium, high, urgent)
        created_at: Timestamp of ticket creation
    """

    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(String(30), nullable=False, default="open")
    priority: Mapped[str] = mapped_column(String(30), nullable=False, default="medium")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )
