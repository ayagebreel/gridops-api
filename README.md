# GridOps API

## Problem

Utility maintenance teams need a reliable way to track network faults and manage maintenance work orders.

Without a centralized system, fault reports, work assignments, required components, and maintenance statuses can become difficult to track and coordinate.

GridOps provides a REST API that allows technicians to report faults, supervisors to create work orders, manage required components, and track work order progress through controlled status transitions.

## Main Features

- Fault reporting
- Work order management
- Component management
- Work order component tracking
- Controlled work order status transitions
- Automated tests
- Dockerized application deployment
- PostgreSQL database integration
- Database healthcheck and startup dependency management

## Technology Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- PostgreSQL 16
- Docker
- Docker Compose
- Pytest
- HTTPX
- Psycopg
- Ruff

## Project Structure

```text
gridops-api/
├── app/
├── tests/
├── docs/
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── requirements.txt
└── README.md
```

## Run with Docker

### Prerequisites

Make sure the following tools are installed:

- Docker
- Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/ayagebreel/gridops-api.git
cd gridops-api
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
POSTGRES_PASSWORD=your_secure_password
```

Use your own secure password.

Do not commit the `.env` file to Git.

### 3. Start the application

Run:

```bash
docker compose up --build
```

Docker Compose starts:

- FastAPI application
- PostgreSQL 16 database

The API waits until PostgreSQL passes its healthcheck before starting.

### 4. Access the API

Open the interactive API documentation:

http://localhost:8000/docs

### 5. View application logs

```bash
docker compose logs api
```

### 6. Run automated tests

```bash
docker compose run --rm api pytest -v
```

### 7. Connect to PostgreSQL

To inspect the database tables:

```bash
docker compose exec db psql -U grid -d gridops -c "\dt"
```

### 8. Stop the application

Press `Ctrl+C` or run:

```bash
docker compose down
```

The named PostgreSQL volume preserves database data when containers are stopped or recreated.

Do not use `docker compose down -v` unless you intentionally want to delete the database volume and its data.

## Running Tests

The automated test suite uses an in-memory SQLite database through SQLAlchemy test fixtures.

Tests can be executed inside the API container using:

```bash
docker compose run --rm api pytest -v
```

## Architecture Decisions

Important architectural decisions and business rules are documented in:

- `docs/decisions.md`
- `docs/incident-01.md`

These documents explain work order status transitions, Docker configuration decisions, and the database startup race condition encountered during development.