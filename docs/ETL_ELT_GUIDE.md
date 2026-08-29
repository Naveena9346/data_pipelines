# ETL & ELT Processing Guide — DataForge

## ETL vs ELT Paradigms

DataForge natively supports both **ETL (Extract, Transform, Load)** and **ELT (Extract, Load, Transform)** processing paradigms:

| Metric / Aspect | ETL Architecture | ELT Architecture |
| :--- | :--- | :--- |
| **Primary Computation** | In-Memory Polars / Celery Worker | Target Data Warehouse (DuckDB / Snowflake / Postgres) |
| **Data Flow** | Source -> Engine -> Target | Source -> Target Storage -> SQL Transformation |
| **Best Used For** | Sensitive data scrubbing, external file processing, schema normalization | Large relational datasets, data warehousing, high-volume analytics |

## Polars Transformation Architecture

DataForge leverages Polars for fast parallelized in-memory ETL operations:
- **Lazy Evaluation**: Queries are optimized using lazy execution graphs prior to memory allocation.
- **Columnar Arrow Memory**: Native Apache Arrow memory layout ensures zero-copy IPC data transfer.

```python
# Polars Transformation Pipeline Pipeline Code Pattern
import polars as pl

def execute_etl_transform(input_df: pl.DataFrame) -> pl.DataFrame:
    return (
        input_df.lazy()
        .filter(pl.col("status") == "ACTIVE")
        .with_columns([
            pl.col("amount").cast(pl.Float64),
            (pl.col("price") * pl.col("quantity")).alias("total_value"),
            pl.col("created_at").str.to_datetime()
        ])
        .collect()
    )
```

## DuckDB ELT SQL Architecture

DuckDB is embedded into DataForge to provide high-speed analytical ELT execution directly on disk or Parquet files without external database overhead:

```sql
-- DuckDB Analytical ELT SQL Pipeline Code Pattern
CREATE TABLE analytics_summary AS
SELECT 
    customer_id,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS lifetime_value,
    AVG(total_amount) AS average_order_value,
    MAX(created_at) AS last_purchase_date
FROM read_parquet('s3://data-lake/orders/*.parquet')
WHERE status = 'COMPLETED'
GROUP BY customer_id
HAVING SUM(total_amount) > 1000;
```
