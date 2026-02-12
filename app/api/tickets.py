from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketOut

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    ticket = Ticket(
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        status="open",
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get("", response_model=list[TicketOut])
def list_tickets(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    return (
        db.query(Ticket)
        .order_by(Ticket.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
