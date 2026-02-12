from fastapi import FastAPI
from sqlalchemy import text

from app.api.tickets import router as tickets_router
from app.db.database import engine

app = FastAPI(title="Incident & Ticket Management API", version="0.1.0")

app.include_router(tickets_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/db-health")
def db_health_check():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"db": "ok"}
