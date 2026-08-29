from typing import Dict, Any
import polars as pl
import duckdb
from app.core.exceptions import ValidationError


class DuckDBTransformationEngine:
    """DuckDB in-memory OLAP SQL transformation engine."""

    @staticmethod
    def execute_sql(input_df: pl.DataFrame, sql_query: str, table_alias: str = "input_table") -> pl.DataFrame:
        try:
            conn = duckdb.connect(database=":memory:")
            # Register Polars Arrow table in DuckDB
            arrow_table = input_df.to_arrow()
            conn.register(table_alias, arrow_table)
            
            arrow_table_res = conn.execute(sql_query).to_arrow_table()
            conn.close()
            return pl.from_arrow(arrow_table_res)
        except Exception as e:
            raise ValidationError(f"DuckDB SQL Transformation Error: {str(e)}")
