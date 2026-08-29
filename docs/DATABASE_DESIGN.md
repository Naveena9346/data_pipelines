# Database Design & Schema Documentation — DataForge

## Entity-Relationship Diagram (ERD) Overview

DataForge uses PostgreSQL 16 for metadata, workflow topology, execution history, and audit logging.

```
+----------------+      +-------------------+      +---------------------+
|     roles      |----->|       users       |----->|     audit_logs      |
+----------------+      +-------------------+      +---------------------+
                                  |
                                  v
                        +-------------------+
                        |     pipelines     |
                        +-------------------+
                          /               \
                         v                 v
            +-------------------+   +--------------------+
            |   pipeline_nodes  |   |   pipeline_edges   |
            +-------------------+   +--------------------+
                         |
                         v
            +-------------------------+
            |   pipeline_executions   |
            +-------------------------+
                         |
                         v
            +-------------------------+
            |     task_executions     |
            +-------------------------+
                         |
                         v
            +-------------------------+
            |     execution_logs      |
            +-------------------------+
```

## Schema Definitions

### 1. User Authentication & Roles (`users`, `roles`, `permissions`)
- `users`: ID, email, hashed_password, full_name, role_id, is_active, created_at, updated_at.
- `roles`: ID, name (`SUPER_ADMIN`, `ADMIN`, `DATA_ENGINEER`, `DATA_ANALYST`, `DEVELOPER`, `VIEWER`), description.
- `role_permissions`: Role-to-permission mapping table.

### 2. Data Sources & Datasets (`data_sources`, `datasets`)
- `data_sources`: ID, name, source_type (`POSTGRES`, `MYSQL`, `S3`, `FILE`, `REST_API`), encrypted_connection_config, created_by, created_at.
- `datasets`: ID, source_id, dataset_name, schema_definition (JSONB), format, row_count, file_size_bytes.

### 3. Pipeline DAG Definitions (`pipelines`, `pipeline_nodes`, `pipeline_edges`)
- `pipelines`: ID, name, description, cron_schedule, is_active, retry_count, timeout_seconds, created_by, created_at.
- `pipeline_nodes`: ID, pipeline_id, node_key, node_type, config_json (JSONB), position_x, position_y.
- `pipeline_edges`: ID, pipeline_id, source_node_key, target_node_key, condition_expr.

### 4. Pipeline Execution History (`pipeline_executions`, `task_executions`, `execution_logs`)
- `pipeline_executions`: ID, pipeline_id, status (`PENDING`, `RUNNING`, `SUCCESS`, `FAILED`), started_at, finished_at, duration_ms, triggered_by.
- `task_executions`: ID, execution_id, node_key, status, input_rows, output_rows, error_message, started_at, finished_at.
- `execution_logs`: ID, task_execution_id, log_level (`DEBUG`, `INFO`, `WARNING`, `ERROR`), log_message, timestamp.

### 5. Quality Reports & Auditing (`data_quality_reports`, `audit_logs`)
- `data_quality_reports`: ID, execution_id, total_rules, passed_rules, failed_rules, metrics_json (JSONB).
- `audit_logs`: ID, user_id, action, resource_type, resource_id, ip_address, user_agent, timestamp.
