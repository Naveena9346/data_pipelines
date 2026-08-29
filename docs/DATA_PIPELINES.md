# Data Pipelines Technical Manual — DataForge

## Pipeline DAG Model

In DataForge, a pipeline is represented as a Directed Acyclic Graph (DAG) consisting of:
- **Nodes**: Specific atomic processing units (Extractors, Quality Checkers, Transformers, Loaders, Alerts).
- **Edges**: Directional dependencies specifying data flow and execution order between nodes.

## Node Classifications

```
[ Extractor Node ] ---> [ Validation Node ] ---> [ Transformation Node ] ---> [ Loader Node ]
```

### 1. Extractor Nodes (Ingestion)
- **Database Extractor**: Executes SQL queries against PostgreSQL, MySQL, SQLite, or Snowflake.
- **CSV/JSON/Parquet Extractor**: Ingests structured and semi-structured files with automated schema inference.
- **API Extractor**: Connects to external REST APIs with pagination, auth headers, and response parsing.

### 2. Validation & Quality Nodes
- **Schema Validator**: Enforces strict column data types, missing column detection, and null tolerances.
- **Rules Checker**: Evaluates non-null constraints, unique key checks, regex patterns, and range assertions.

### 3. Transformation Nodes
- **SQL Operator**: Executes DuckDB SQL expressions (`SELECT`, `JOIN`, `GROUP BY`, `WINDOW`, `CASE WHEN`).
- **Column Mutator**: Renames, casts, converts, or computes derived columns using Polars expression syntax.
- **Filter & Deduplicator**: Drops duplicate rows, filters outliers, and handles missing values (`FILLNA`, `DROPNA`).

### 4. Loader Nodes (Sinks)
- **Database Sink**: Inserts/upserts transformed data into target database tables with transaction isolation.
- **File Sink**: Exports data to compressed Parquet, CSV, or JSON formats.

## Execution Lifecycle States

1. `PENDING`: Pipeline queued for execution.
2. `COMPILING`: DAG topology verified for cycles and dependencies resolved.
3. `RUNNING`: Tasks actively executing across Celery worker nodes.
4. `SUCCESS`: All DAG nodes completed successfully.
5. `FAILED`: One or more critical DAG nodes failed after exhausting configured retry attempts.
6. `CANCELLED`: Execution manually terminated by an authorized user.
