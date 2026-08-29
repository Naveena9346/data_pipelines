# Deployment & Operations Guide — DataForge

## Containerized Docker Deployment

DataForge is fully containerized using Docker Compose for production deployments.

### 1. Build & Launch Stack

```bash
docker-compose up --build -d
```

### 2. Apply Database Migrations

```bash
docker-compose exec backend alembic upgrade head
```

### 3. Seed Initial Super Admin & System Roles

```bash
docker-compose exec backend python -m app.scripts.seed_db
```

## Production Security Best Practices

1. Change `SECRET_KEY` and `ENCRYPTION_KEY` in `backend/.env`.
2. Configure TLS/SSL termination with Nginx or Traefik reverse proxy.
3. Restrict PostgreSQL and Redis network interfaces to private VPC subnets.
