# Architecture Specification — DataForge Platform

## System Topology & Micro-Modular Design

DataForge is architected as a modular, decoupled data engineering platform designed for scalability, low latency execution, and resilient operational monitoring.

```
+-----------------------------------------------------------------------+
|                            USER INTERFACE                             |
|       React 18 + TypeScript + Vite + TailwindCSS + React Flow         |
+-----------------------------------------------------------------------+
                                   |
                             HTTP / REST APIs
                                   v
+-----------------------------------------------------------------------+
|                           CONTROL PLANE API                           |
|      FastAPI Async Engine + Pydantic Schemas + SQLAlchemy ORM        |
+-----------------------------------------------------------------------+
          |                        |                        |
  Database Access          Task Dispatch            Metrics Stream
          v                        v                        v
+------------------+    +-------------------+    +----------------------+
|  PostgreSQL 16   |    |      Redis 7      |    |  OpenTelemetry Logs  |
| Metadata & Audit |    | Message & Broker  |    | & Audit Streamer     |
+------------------+    +-------------------+    +----------------------+
                                   |
                             Celery Worker
                                   v
+-----------------------------------------------------------------------+
|                        DATA PROCESSING PLANE                          |
|    Polars Engine + DuckDB OLAP SQL + PyArrow Columnar Extractors      |
+-----------------------------------------------------------------------+
                                   |
                        Target Sinks & Storage
                                   v
+-----------------------------------------------------------------------+
|              PostgreSQL / MySQL / Snowflake / S3 / Local              |
+-----------------------------------------------------------------------+
```

## Modular Layers

### 1. Control Plane (FastAPI)
The API service acts as the orchestration brain. It manages identity authentication (JWT), RBAC authorization, CRUD operations for datasets and pipelines, DAG graph validation (cycle checking via Kahn's algorithm), and dispatching task executions to the broker.

### 2. Execution Engine (Celery + Polars + DuckDB)
- **Celery Workers**: Run background tasks asynchronously outside the API request-response loop.
- **Polars Engine**: Handles fast columnar operations on CSV, JSON, Parquet, and Excel data in memory.
- **DuckDB Engine**: Executes complex SQL analytical transformations, joins, and aggregations directly on local or cloud datasets with zero memory copy overhead.

### 3. Messaging & State Management (Redis)
Redis serves a dual role as the high-throughput Celery message broker and the ephemeral result state backend for real-time task progress updates.

### 4. Metadata & Audit Store (PostgreSQL 16)
All operational state—including user profiles, role definitions, data source credentials (AES encrypted), pipeline topologies, execution history, data quality reports, and system audit logs—is stored in a relational PostgreSQL database.
