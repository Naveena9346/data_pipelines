# DataForge — Enterprise Data Pipelines & Data Engineering Platform

DataForge is a high-performance, enterprise-grade Data Pipelines and Data Engineering Platform designed to create, execute, monitor, transform, and analyze large-scale data workflows. Built with a modern micro-modular architecture, DataForge enables Data Engineers, Data Analysts, Developers, and System Administrators to manage complex ETL and ELT data pipelines with robust validation, fault tolerance, role-based security, and real-time operational monitoring.

---

## Key Features

- **Multi-Role Authentication & Security**: Granular Role-Based Access Control (RBAC) supporting Super Admin, Admin, Data Engineer, Data Analyst, Developer, and Viewer roles with JWT authentication and strict scope enforcement.
- **Visual DAG Pipeline Builder**: Interactive drag-and-drop workflow canvas built with React Flow for designing complex directed acyclic graphs (DAGs) with dependencies, branching, and conditional triggers.
- **High-Throughput Transformation Engine**: Embedded Polars columnar engine and DuckDB OLAP SQL engine supporting fast in-memory transformation, filtering, joining, aggregation, and Parquet/CSV file operations.
- **Universal Data Connectors**: Built-in support for relational databases (PostgreSQL, MySQL, SQLite, Snowflake), semi-structured files (CSV, JSON, NDJSON, Parquet, Excel), cloud storage (AWS S3, Local Data Lake), and REST API endpoints.
- **Automated Data Quality & Validation Engine**: Configurable schema enforcement, regex pattern matching, non-null assertions, numeric range checks, unique key constraints, and dynamic anomaly detection with automated quality reporting.
- **Orchestration & Task Queue**: Celery distributed worker execution pool powered by Redis event broker with automatic retry mechanisms, exponential backoff, configurable timeout limits, and failure recovery.
- **Flexible Job Scheduling**: APScheduler integration supporting cron expressions, fixed intervals, calendar events, and manual REST API execution triggers.
- **Real-Time Dashboards & Analytics**: Operational metrics tracking total, running, successful, and failed pipeline runs, execution latency, throughput, error rates, system performance, and audit trails.
- **Comprehensive Audit Trail & Logging**: Detailed execution log capture, stdout/stderr isolation per task step, and audit tracking of user actions for regulatory compliance.

---

## Tech Stack & Architecture

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy 2.0 (Async ORM), Pydantic v2, Alembic, Celery, APScheduler, Structlog.
- **Data Engines**: Polars, DuckDB, PyArrow, Pandas.
- **Frontend**: React 18, TypeScript, Vite, TailwindCSS, React Flow, Recharts, TanStack Query (React Query v5), Zustand.
- **Database & Cache**: PostgreSQL 16 (Metadata & Audit Storage), Redis 7 (Broker & Session Cache), DuckDB (OLAP Engine).
- **DevOps & Testing**: Docker, Docker Compose, PyTest (Async & Fixtures), Jest, GitHub Actions CI/CD.

---

## Directory Layout

```
data-pipelines-platform/
├── backend/                  # Python FastAPI Server & Execution Engine
│   ├── app/                  # Core App, Domain Modules, Models & REST APIs
│   └── tests/                # Automated Unit, Integration & API Test Suite
├── frontend/                 # React 18 / TypeScript Web Client
│   ├── src/                  # React Flow Canvas, Dashboards, Controls & Services
├── docs/                     # System Architecture, Database & API Specifications
├── docker-compose.yml        # Docker Multi-Container Infrastructure
└── README.md                 # System Overview & Quickstart Guide
```

---

## Getting Started

### Prerequisites

- **Python**: 3.11 or higher
- **Node.js**: v18.0 or higher
- **Docker & Docker Compose**: (Recommended for running PostgreSQL and Redis)

### Setup Instructions

For detailed step-by-step setup, configuration, and environment instructions, please refer to the documentation files in the `docs/` folder:

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Data Pipelines & Engine Guide](docs/DATA_PIPELINES.md)
- [ETL/ELT Technical Manual](docs/ETL_ELT_GUIDE.md)
- [Database Schema & Design](docs/DATABASE_DESIGN.md)
- [API Documentation](docs/API_DOCUMENTATION.md)
- [Environment Configuration](docs/ENVIRONMENT.md)
- [Testing & Quality Assurance](docs/TESTING.md)
- [Deployment & CI/CD](docs/DEPLOYMENT.md)

---

## License

Enterprise Proprietary License. All rights reserved.
