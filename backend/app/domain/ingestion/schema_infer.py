from typing import Dict, Any, List
import polars as pl


class SchemaInferEngine:
    """Infer column data types, nullability, and summary stats for datasets."""

    @staticmethod
    def infer_schema_from_df(df: pl.DataFrame) -> List[Dict[str, Any]]:
        schema_list = []
        for col_name, dtype in df.schema.items():
            null_count = df[col_name].null_count()
            schema_list.append({
                "column_name": col_name,
                "data_type": str(dtype),
                "nullable": null_count > 0,
                "null_count": null_count
            })
        return schema_list
