# Docker Setup for Finance API

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Application Settings
APP_NAME=Finance API
APP_VERSION=1.0.0
APP_DESCRIPTION=Finance API
DEBUG=True

# Database Configuration
DATABASE_URL=postgresql+asyncpg://myuser:mypassword@postgres:5432/mydb

# Security Settings
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30

# Redis Configuration (optional)
REDIS_URL=redis://redis:6379/0
```

## Quick Start

1. **Build and run all services:**
   ```bash
   docker-compose up --build
   ```

2. **Run in background:**
   ```bash
   docker-compose up -d --build
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f fastapi
   ```

4. **Stop services:**
   ```bash
   docker-compose down
   ```

## Services

- **FastAPI App**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432
- **PgAdmin**: http://localhost:5050 (admin@finance.com / admin)
- **Redis**: localhost:6379

## Database Management

The application will automatically run Alembic migrations on startup. If you need to run migrations manually:

```bash
docker-compose exec fastapi alembic upgrade head
```

## Development

For development with hot reload, the FastAPI service is configured to watch for file changes and restart automatically.
