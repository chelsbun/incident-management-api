# Incident & Ticket Management API

Production-grade backend service for enterprise incident and ticket management. Built with FastAPI, PostgreSQL, and professional engineering practices.

## Features

- **RESTful API** with versioned endpoints (`/api/v1`)
- **Standardized response envelope** for consistent client integration
- **JWT-ready architecture** (auth endpoints coming soon)
- **Database migrations** via Alembic for schema version control
- **Dockerized PostgreSQL** for consistent dev/prod environments
- **Type-safe** with Pydantic schemas and SQLAlchemy 2.0 ORM
- **Health checks** for API and database connectivity
- **Comprehensive error handling** without exposing sensitive details

## Tech Stack

- **Framework**: FastAPI 0.128+
- **Database**: PostgreSQL 16 (Docker)
- **ORM**: SQLAlchemy 2.0 with async support
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Python**: 3.11+

## Project Structure

```
ibm-incident-api/
├── app/
│   ├── api/              # API route handlers
│   │   └── tickets.py    # Ticket endpoints
│   ├── core/             # Core configuration
│   │   └── config.py     # Environment settings
│   ├── db/               # Database setup
│   │   └── database.py   # Engine, session, base
│   ├── models/           # SQLAlchemy ORM models
│   │   └── ticket.py
│   ├── schemas/          # Pydantic request/response models
│   │   ├── ticket.py
│   │   └── response.py   # Standard envelope
│   └── main.py           # FastAPI application
├── alembic/              # Database migrations
│   ├── versions/
│   └── env.py
├── .env.example          # Environment template
├── docker-compose.yml    # PostgreSQL container
└── requirements.txt      # Python dependencies
```

## Getting Started

### Prerequisites

- **Python 3.11+**
- **Docker Desktop** (for PostgreSQL)
- **Git**

### 1. Clone and Setup

```powershell
# Clone repository
git clone <repo-url>
cd ibm-incident-api

# Create virtual environment
python -m venv .venv

# Activate venv (Windows PowerShell)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```powershell
# Copy environment template
cp .env.example .env

# Edit .env and set your database password
# DATABASE_URL=postgresql+psycopg2://incident_user:YOUR_PASSWORD@localhost:5432/incident_db
```

### 3. Start Database

```powershell
# Start PostgreSQL container
docker compose up -d

# Verify container is running
docker ps
```

**Troubleshooting**: If you see `dockerDesktopLinuxEngine` pipe errors:
- Ensure Docker Desktop is running (check system tray)
- Run: `docker context use default`
- Restart Docker Desktop if needed

### 4. Run Migrations

```powershell
# Apply database migrations
alembic upgrade head

# Verify tables created
docker exec -it incident_db psql -U incident_user -d incident_db -c "\dt"
```

### 5. Start API Server

```powershell
# Start development server with hot reload
uvicorn app.main:app --reload
```

The API will be available at: **http://127.0.0.1:8000**

## API Documentation

### Interactive Docs

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Response Format

All endpoints return a standardized envelope:

```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "message": "Success"
}
```

### Endpoints

#### Health Checks

**GET** `/health` - Verify API is running
**GET** `/db-health` - Verify database connectivity

#### Tickets (v1)

**POST** `/api/v1/tickets` - Create a new ticket

```json
{
  "title": "Server down in production",
  "description": "EU-West-1 instances not responding",
  "priority": "urgent"
}
```

**GET** `/api/v1/tickets` - List tickets with pagination

Query params:
- `limit` (default: 20, max: 100)
- `offset` (default: 0)

Response includes ticket details with timestamps.

## Development Commands

### Database & API

```powershell
# Start database
docker compose up -d

# Stop database
docker compose down

# Activate virtual environment
.venv\Scripts\activate

# Run API server
uvicorn app.main:app --reload

# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Check current migration
alembic current

# View database tables
docker exec -it incident_db psql -U incident_user -d incident_db -c "\dt"
```

### Code Quality

```powershell
# Install dev dependencies
pip install -r requirements-dev.txt

# Run linter (auto-fix)
ruff check . --fix

# Format code
black .

# Type checking
mypy app

# Run all quality checks
ruff check . && black --check . && mypy app && pytest
```

### Pre-commit Hooks (Optional)

```powershell
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

## Testing

```powershell
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_health.py

# Run specific test function
pytest tests/test_tickets.py::test_create_ticket_success
```

Tests use SQLite in-memory database for fast execution without requiring PostgreSQL.

## Environment Variables

Required variables (see `.env.example`):

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+psycopg2://user:pass@localhost:5432/dbname` |
| `POSTGRES_USER` | Database username | `incident_user` |
| `POSTGRES_PASSWORD` | Database password | `your_secure_password` |
| `POSTGRES_DB` | Database name | `incident_db` |

## Security

- ✅ No hardcoded secrets in codebase
- ✅ Environment-driven configuration
- ✅ Parameterized SQL queries (SQLAlchemy ORM)
- ✅ Input validation via Pydantic
- ✅ Safe error messages (no stack traces to clients)
- ⏳ Authentication & authorization (coming soon)

## Roadmap

- [ ] GET `/api/v1/tickets/{id}` with 404 handling
- [ ] PATCH `/api/v1/tickets/{id}` for updates
- [ ] PATCH `/api/v1/tickets/{id}/status` for status transitions
- [ ] Ticket events audit trail
- [ ] Full-text search and filtering
- [ ] JWT authentication
- [ ] Role-based access control (RBAC)
- [ ] Rate limiting
- [ ] Structured logging (JSON)

## Contributing

This project follows strict professional development practices:

- Small, incremental changes (≤50 lines per commit)
- One feature per pull request
- All changes verified before commit
- Conventional commit messages (`feat:`, `fix:`, `docs:`, etc.)

## License

[Add your license here]

## Contact

[Add contact information]
