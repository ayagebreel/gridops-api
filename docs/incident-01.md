# Incident 01: Database Startup Race Condition

## 1. Incident Summary

During the initial Docker Compose setup, the FastAPI application attempted to connect to PostgreSQL before the database was ready to accept connections.

This caused the API container to exit with a database connection error.

## 2. Root Cause

The API service initially used the short syntax of `depends_on`:

```yaml
depends_on:
  - db
```

This only controls service startup order. It does not guarantee that PostgreSQL is ready to accept connections.

The application executes:

```python
Base.metadata.create_all(bind=engine)
```

during application import, which requires an active database connection.

As a result, the API attempted to connect while PostgreSQL was still starting.

## 3. Reproducing the Issue

To reproduce the issue:

1. Temporarily removed the database healthcheck dependency condition.
2. Added a temporary startup delay to PostgreSQL.
3. Started the services using Docker Compose.

The API failed with:

```text
psycopg.OperationalError:
connection refused
```

The PostgreSQL container became ready afterward, confirming that the API had attempted to connect too early.

## 4. Resolution

Restored the PostgreSQL healthcheck and updated the API dependency:

```yaml
depends_on:
  db:
    condition: service_healthy
```

The healthcheck uses:

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB"]
  interval: 5s
  timeout: 5s
  retries: 5
  start_period: 10s
```

## 5. Verification

After restoring the configuration, the services started successfully.

Observed logs:

```text
Container gridops-api-db-1 Healthy
Application startup complete.
Uvicorn running on http://0.0.0.0:8000
```

## 6. Lessons Learned

- Container startup does not necessarily mean application readiness.
- `depends_on` short syntax does not wait for database readiness.
- Healthchecks help determine when a service is ready.
- `condition: service_healthy` prevents dependent services from starting before their dependencies are healthy.
- Database connection initialization during application import makes startup ordering especially important.