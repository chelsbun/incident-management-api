"""
Database connection and session management.

Provides SQLAlchemy engine, session factory, and base model class.
Uses dependency injection pattern for database sessions in FastAPI.

Author: Project
Last Modified: 2026-02-12
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


def get_db():
    """
    Database session dependency for FastAPI.

    Yields a database session and ensures it's closed after request.
    Use with Depends(get_db) in route handlers.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
