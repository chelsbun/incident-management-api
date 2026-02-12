Incident & Ticket Management API
Project Description + Current Status
====================================

PROJECT OVERVIEW
----------------
This project is a production-style backend service for an enterprise incident
and ticket management system. It is designed to demonstrate real-world backend
engineering practices including API design, database modeling, migrations,
Docker-based infrastructure, and clean separation of concerns.

The goal is to build something that resembles an internal IT operations tool
rather than a basic tutorial application.

Tech stack:
- FastAPI
- PostgreSQL (Docker)
- SQLAlchemy ORM
- Alembic migrations
- Pydantic schemas

This project is intended to showcase professional readiness for backend and
platform engineering roles.


CURRENT ARCHITECTURE
--------------------
ibm-incident-api/
  app/
    main.py
    api/
      tickets.py
    core/
      config.py
    db/
      database.py
    models/
      ticket.py
    schemas/
      ticket.py
  alembic/
    env.py
    versions/
  alembic.ini
  docker-compose.yml
  requirements.txt
  README.md
  .env


INFRASTRUCTURE
--------------
PostgreSQL runs in Docker using docker-compose.

Container name: incident_db  
Port mapping: 5432 → 5432  
Persistent volume: incident_pgdata

Environment configuration is stored in `.env`.

Example DATABASE_URL:
postgresql+psycopg2://incident_user:incident_pass@localhost:5432/incident_db


DATABASE STATUS
---------------
Alembic is initialized and functional.

Migrations are being used correctly instead of automatic table creation.

The database currently contains:
- alembic_version
- tickets

The tickets table includes:
- id (primary key, indexed)
- title (required)
- description (optional)
- status (default = "open")
- priority (default = "medium")
- created_at (timestamp)


API STATUS
----------
The API server runs locally via:

uvicorn app.main:app --reload

Swagger docs:
http://127.0.0.1:8000/docs


Operational endpoints:
- GET /health → confirms API is running
- GET /db-health → confirms database connectivity


Ticket endpoints:
- POST /tickets
  Creates a ticket in Postgres.
  Returns 201 with the stored record including id and timestamps.

- GET /tickets
  Returns tickets ordered by newest first.
  Supports pagination via limit and offset.

Both endpoints have been tested successfully.
Tickets are persisting in the database.


WHAT HAS BEEN VERIFIED
----------------------
✓ FastAPI server runs  
✓ Docker Postgres running  
✓ Database connection working  
✓ Alembic configured  
✓ Migration created and applied  
✓ tickets table exists  
✓ POST creates records  
✓ GET retrieves records  
✓ Swagger functioning  


DEVELOPMENT PHILOSOPHY
----------------------
This project follows professional backend design patterns.

- Separation between API, models, schemas, and database logic
- Environment-driven configuration
- Migrations for schema control
- Containerized infrastructure
- Incremental feature delivery


NEXT FEATURES TO BUILD
----------------------
Priority roadmap (in order of impact):

1. GET /tickets/{id} with proper 404 handling
2. PATCH /tickets/{id} to edit title/description/priority
3. PATCH /tickets/{id}/status with lifecycle rules
4. ticket_events audit table (who changed what and when)
5. filtering and search
6. authentication / RBAC
7. structured logging and monitoring readiness


HOW TO RESUME DEVELOPMENT LATER
-------------------------------
1. Start Docker:
   docker compose up -d

2. Activate virtual environment:
   .venv\Scripts\activate

3. Run API:
   uvicorn app.main:app --reload

4. Open Swagger:
   http://127.0.0.1:8000/docs


CURSOR WORKFLOW RULES
---------------------

Core principles:
- Build in small increments
- One feature per commit
- Do not bypass layers
- All DB changes go through Alembic
- Always run and verify in Swagger


When adding a feature:
1. Define the goal in one sentence
2. Identify files that will change
3. Implement minimal working version
4. Run and verify
5. Add validation and error handling
6. Update documentation if needed
7. Commit


Project conventions:
- Routes → app/api
- Schemas → app/schemas
- Models → app/models
- DB session → app/db/database.py
- Config → app/core/config.py
- No hardcoded secrets


API rules:
- Correct status codes
- Use response_model
- Use dependency injection for DB
- Validate inputs


Database rules:
- Never use create_all
- Always create migration
- Inspect generated file
- Upgrade database


Commit prefixes:
feat: new feature
fix: bug
refactor: restructure
chore: tooling
docs: documentation
test: tests


CURRENT PROJECT MATURITY
------------------------
The foundation is complete and production-shaped.

We are past setup and infrastructure and are now entering the stage where
business logic and advanced behaviors will make the project stand out.


GOAL FOR NEXT SESSION
---------------------
Implement GET /tickets/{id} with proper 404 handling, then add PATCH endpoints
for updates and status transitions. Keep changes small and verify in Swagger
after each step.

STARTUP (always do this first)
------------------------------
1) Open terminal in project root:
   cd C:\Users\chels\ibm-incident-api

2) Start Postgres:
   docker compose up -d

3) Activate venv:
   .venv\Scripts\activate

4) Run API:
   uvicorn app.main:app --reload

5) Open Swagger:
   http://127.0.0.1:8000/docs


STEP 1: Add GET /tickets/{id}
-----------------------------
File: app/api/tickets.py

Add imports if missing:
from fastapi import HTTPException

Add endpoint:
@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

VERIFY:
- Swagger: GET /tickets/{ticket_id}
- Test with an existing id (ex: 1 or 2) -> 200 + ticket
- Test with 999 -> 404 Ticket not found


STEP 2: Add PATCH /tickets/{id} (edit title/description/priority)
-----------------------------------------------------------------
Create schema file update:
File: app/schemas/ticket.py

Add:
from pydantic import BaseModel, Field

class TicketUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    priority: str | None = Field(default=None, pattern="^(low|medium|high|urgent)$")

Then in app/api/tickets.py add:
@router.patch("/{ticket_id}", response_model=TicketOut)
def update_ticket(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Tic

