# REST API Specification — DataForge

All API endpoints are prefixed with `/api/v1` and require an `Authorization: Bearer <JWT_TOKEN>` header except `/api/v1/auth/login` and `/api/v1/auth/register`.

## Authentication Endpoints

- `POST /api/v1/auth/register` — User self-registration (Default role: Viewer / Developer).
- `POST /api/v1/auth/login` — User authentication. Returns JWT token and user profile.
- `GET /api/v1/auth/me` — Retrieve current authenticated user session details and permissions.

## Data Source & Dataset Endpoints

- `GET /api/v1/sources` — List all registered data sources.
- `POST /api/v1/sources` — Create new data source (Postgres, MySQL, CSV, S3, API).
- `POST /api/v1/sources/{id}/test` — Test connectivity to data source.
- `GET /api/v1/datasets` — List registered datasets and infer dynamic schemas.
- `POST /api/v1/datasets/upload` — Upload CSV/JSON file to dataset repository.

## Pipeline Management & DAG Builder Endpoints

- `GET /api/v1/pipelines` — Search, filter, and paginate data pipelines.
- `POST /api/v1/pipelines` — Create a new pipeline DAG.
- `GET /api/v1/pipelines/{id}` — Fetch pipeline DAG nodes, edges, and configuration.
- `PUT /api/v1/pipelines/{id}` — Update pipeline topology or parameters.
- `DELETE /api/v1/pipelines/{id}` — Delete pipeline.
- `POST /api/v1/pipelines/{id}/validate` — Verify pipeline topology for cycles and configuration errors.

## Pipeline Execution & Scheduler Endpoints

- `POST /api/v1/pipelines/{id}/execute` — Trigger immediate manual pipeline execution.
- `POST /api/v1/executions/{id}/cancel` — Cancel an in-progress pipeline execution.
- `GET /api/v1/executions` — List execution history with status filters.
- `GET /api/v1/executions/{id}` — Retrieve detailed execution metrics, task breakdown, and status.
- `GET /api/v1/executions/{id}/logs` — Stream or retrieve task logs.

## Monitoring, Metrics & Quality Reports Endpoints

- `GET /api/v1/monitoring/metrics` — Aggregate system execution metrics (throughput, error rate, latency).
- `GET /api/v1/monitoring/audit-logs` — Query system audit trail logs.
- `GET /api/v1/quality/reports/{execution_id}` — Retrieve data quality check results and anomalies.
