import os
from typing import Dict, Any, Tuple
import polars as pl
import duckdb
from app.core.exceptions import ValidationError


class IngestionExtractor:
    """Core extractor for reading datasets into Polars DataFrames."""

    @staticmethod
    def extract_file(file_path: str, format_type: str) -> pl.DataFrame:
        if not os.path.exists(file_path):
            raise ValidationError(f"Extraction failed: file '{file_path}' does not exist.")

        format_clean = format_type.upper().replace("_FILE", "")
        try:
            if format_clean == "CSV":
                return pl.read_csv(file_path)
            elif format_clean == "JSON":
                return pl.read_json(file_path)
            elif format_clean == "PARQUET":
                return pl.read_parquet(file_path)
            else:
                raise ValidationError(f"Unsupported file format '{format_type}' for extraction.")
        except Exception as e:
            raise ValidationError(f"Failed to extract file dataset '{file_path}': {str(e)}")

    @staticmethod
    def extract_duckdb_query(query: str, db_path: str = ":memory:") -> pl.DataFrame:
        try:
            conn = duckdb.connect(database=db_path)
            arrow_table = conn.execute(query).fetch_record_batch()
            conn.close()
            return pl.from_arrow(arrow_table)
        except Exception as e:
            raise ValidationError(f"DuckDB SQL extraction failed: {str(e)}")
