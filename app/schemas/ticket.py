from datetime import datetime
from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    priority: str = Field(default="medium", pattern="^(low|medium|high|urgent)$")


class TicketOut(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    priority: str
    created_at: datetime

    class Config:
        from_attributes = True
