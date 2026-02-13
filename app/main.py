"""
FastAPI application entry point.

Main application module that:
- Configures the FastAPI application
- Registers exception handlers for consistent error responses
- Mounts API routers with versioning
- Provides health check endpoints

Author: Project
Last Modified: 2026-02-12
"""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api.tickets import router as tickets_router
from app.db.database import engine
from app.schemas.response import ApiResponse, error_response, success_response

app = FastAPI(title="Incident & Ticket Management API", version="0.1.0")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTPException and return in envelope format."""
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            error=exc.detail, message=f"Request failed: {exc.detail}"
        ).model_dump(),
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors safely without exposing internal details."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(
            error="Database error", message="An error occurred while processing your request"
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors safely."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(
            error="Internal server error", message="An unexpected error occurred"
        ).model_dump(),
    )


# Mount API v1 routes
app.include_router(tickets_router, prefix="/api/v1")


@app.get("/health", response_model=ApiResponse[dict])
def health_check():
    """Health check endpoint - verifies API is running."""
    return success_response(data={"status": "ok"}, message="API is healthy")


@app.get("/db-health", response_model=ApiResponse[dict])
def db_health_check():
    """Database health check - verifies DB connectivity."""
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return success_response(data={"db": "ok"}, message="Database is healthy")
