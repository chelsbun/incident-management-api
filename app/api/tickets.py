"""
Ticket API endpoints.

Handles CRUD operations for incident tickets with pagination support.
All endpoints return standardized envelope responses.

Author: Project
Last Modified: 2026-02-12
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.ticket import Ticket
from app.schemas.response import ApiResponse, success_response
from app.schemas.ticket import TicketCreate, TicketOut

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("", response_model=ApiResponse[TicketOut], status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    """Create a new ticket."""
    try:
        ticket = Ticket(
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            status="open",
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return success_response(data=ticket, message="Ticket created successfully")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create ticket due to database error",
        ) from e


@router.get("", response_model=ApiResponse[list[TicketOut]])
def list_tickets(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    """List tickets with pagination."""
    tickets = (
        db.query(Ticket)
        .order_by(Ticket.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return success_response(data=tickets, message=f"Retrieved {len(tickets)} tickets")
