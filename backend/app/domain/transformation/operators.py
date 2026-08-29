from typing import Dict, Any
import polars as pl
from app.domain.transformation.polars_engine import PolarsTransformationEngine
from app.domain.transformation.duckdb_engine import DuckDBTransformationEngine
from app.core.exceptions import ValidationError


def apply_transformation_operator(df: pl.DataFrame, config: Dict[str, Any]) -> pl.DataFrame:
    operator_type = config.get("operator_type", "FILTER")

    if operator_type == "FILTER":
        column = config.get("column")
        operator = config.get("operator", "==")
        value = config.get("value")
        return PolarsTransformationEngine.filter_rows(df, column, operator, value)

    elif operator_type == "SELECT":
        columns = config.get("columns", [])
        return PolarsTransformationEngine.select_columns(df, columns)

    elif operator_type == "RENAME":
        mapping = config.get("mapping", {})
        return PolarsTransformationEngine.rename_columns(df, mapping)

    elif operator_type == "DEDUPLICATE":
        subset = config.get("subset")
        return PolarsTransformationEngine.drop_duplicates(df, subset)

    elif operator_type == "FILL_NULLS":
        strategy = config.get("strategy", "zero")
        custom_value = config.get("custom_value")
        return PolarsTransformationEngine.fill_nulls(df, strategy, custom_value)

    elif operator_type == "SQL":
        sql_query = config.get("sql_query", "SELECT * FROM input_table")
        table_alias = config.get("table_alias", "input_table")
        return DuckDBTransformationEngine.execute_sql(df, sql_query, table_alias)

    else:
        raise ValidationError(f"Unknown transformation operator type '{operator_type}'.")
