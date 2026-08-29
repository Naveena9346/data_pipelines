# Automated Testing Specification — DataForge

DataForge includes comprehensive test suites spanning unit, integration, API, database, and pipeline execution scenarios.

## Executing Backend Tests

```bash
cd backend
pytest -v --cov=app --cov-report=term-missing tests/
```

## Test Suite Categories

1. **Authentication & RBAC Tests (`tests/test_auth.py`)**:
   - User creation, password hashing integrity, JWT bearer token verification.
   - Granular RBAC endpoint protection checks.

2. **Data Ingestion Tests (`tests/test_ingestion.py`)**:
   - CSV, JSON, and Parquet data ingestion.
   - Dynamic schema detection and datatypes inference.

3. **Data Transformation Tests (`tests/test_transformation.py`)**:
   - Polars in-memory transformation, filtering, and aggregation.
   - DuckDB SQL expression processing.

4. **Data Quality Tests (`tests/test_quality.py`)**:
   - Schema enforcement, non-null assertions, regex validation, range checks.
   - Data quality metrics generation.

5. **DAG Engine & Execution Tests (`tests/test_dag_execution.py`)**:
   - Kahn's topological sort and DAG cycle validation.
   - Execution state machine transitions and retry handling.
