# Architecture Decisions

## Work Order Status Transitions

The system supports the following statuses:

- open
- assigned
- in_progress
- closed
- cancelled

## Allowed Transitions

| From | To |
|---|---|
| open | assigned |
| open | cancelled |
| assigned | in_progress |
| assigned | cancelled |
| in_progress | closed |

## Decision: Closed Orders Cannot Be Reopened

A closed work order represents a completed maintenance
operation.

If a new problem occurs after closure, a new fault
and work order should be created.

This preserves the history of maintenance operations
and avoids changing previously completed records.

Cancelled work orders are also terminal.

## Docker Architecture Decisions

### 1. Docker Image Contents

The Docker image includes:

- Python 3.12 runtime.
- Application source code.
- Python dependencies from requirements.txt.
- Application startup command.

These components are included in the image to make the application portable and consistent across environments.

### 2. Environment Variables

Environment-specific configuration is provided at runtime through environment variables.

For example:

- DATABASE_URL
- Database credentials
- Other environment-specific settings.

This allows the same Docker image to run in different environments without rebuilding it for each environment.

When DATABASE_URL is not provided, the application defaults to a local SQLite database.
Docker Compose provides a PostgreSQL DATABASE_URL at runtime.

### 3. Database Persistence

PostgreSQL data is stored in a named Docker volume:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

This ensures database data persists when containers are stopped or recreated.

Database data should not be stored inside the application image.

### 4. Secrets Management

For local development, environment variables are loaded from a `.env` file.

The `.env` file is excluded from Git and Docker build context to prevent accidental exposure of credentials.

In production, secrets should be injected through a secure secrets management solution or deployment environment.

### 5. Non-root Application User

The API container runs as a dedicated non-root user named `appuser`.

This follows the principle of least privilege and reduces the potential impact of application vulnerabilities.