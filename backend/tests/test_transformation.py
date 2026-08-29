import pytest
import polars as pl
from app.domain.transformation.polars_engine import PolarsTransformationEngine
from app.domain.transformation.duckdb_engine import DuckDBTransformationEngine


def test_polars_transformation_filtering():
    df = pl.DataFrame({
        "id": [1, 2, 3, 4],
        "category": ["TECH", "FINANCE", "TECH", "HEALTH"],
        "amount": [500.0, 1200.0, 350.0, 800.0]
    })

    filtered_df = PolarsTransformationEngine.filter_rows(df, "category", "==", "TECH")
    assert filtered_df.height == 2
    assert set(filtered_df["id"]) == {1, 3}


def test_duckdb_sql_transformation():
    df = pl.DataFrame({
        "user_id": [101, 102, 101, 103],
        "spend": [50.0, 100.0, 75.0, 200.0]
    })

    sql = """
    SELECT user_id, SUM(spend) AS total_spend, COUNT(*) AS txn_count
    FROM input_table
    GROUP BY user_id
    HAVING SUM(spend) > 110
    """
    res_df = DuckDBTransformationEngine.execute_sql(df, sql)
    assert res_df.height == 2
    user_ids = set(res_df["user_id"])
    assert user_ids == {101, 103}
