from typing import Dict, Any, List
import polars as pl
from app.core.exceptions import ValidationError


class PolarsTransformationEngine:
    """High-speed Polars columnar transformation engine."""

    @staticmethod
    def filter_rows(df: pl.DataFrame, column: str, operator: str, value: Any) -> pl.DataFrame:
        if column not in df.columns:
            raise ValidationError(f"Filter error: Column '{column}' not found in dataset.")

        col_expr = pl.col(column)
        if operator == "==":
            return df.filter(col_expr == value)
        elif operator == "!=":
            return df.filter(col_expr != value)
        elif operator == ">":
            return df.filter(col_expr > float(value))
        elif operator == "<":
            return df.filter(col_expr < float(value))
        elif operator == ">=":
            return df.filter(col_expr >= float(value))
        elif operator == "<=":
            return df.filter(col_expr <= float(value))
        elif operator == "contains":
            return df.filter(col_expr.str.contains(str(value)))
        else:
            raise ValidationError(f"Unsupported filter operator '{operator}'.")

    @staticmethod
    def select_columns(df: pl.DataFrame, columns: List[str]) -> pl.DataFrame:
        missing = [c for c in columns if c not in df.columns]
        if missing:
            raise ValidationError(f"Select error: Columns {missing} not found in dataset.")
        return df.select(columns)

    @staticmethod
    def rename_columns(df: pl.DataFrame, mapping: Dict[str, str]) -> pl.DataFrame:
        return df.rename(mapping)

    @staticmethod
    def drop_duplicates(df: pl.DataFrame, subset: List[str] = None) -> pl.DataFrame:
        return df.unique(subset=subset)

    @staticmethod
    def fill_nulls(df: pl.DataFrame, strategy: str = "zero", custom_value: Any = None) -> pl.DataFrame:
        if strategy == "zero":
            return df.fill_null(0)
        elif strategy == "forward":
            return df.fill_null(strategy="forward")
        elif strategy == "backward":
            return df.fill_null(strategy="backward")
        elif strategy == "custom":
            return df.fill_null(custom_value)
        return df
