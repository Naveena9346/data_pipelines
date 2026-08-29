import os
import pytest
import polars as pl
from app.domain.ingestion.extractors import IngestionExtractor
from app.domain.ingestion.schema_infer import SchemaInferEngine


def test_csv_file_extraction_and_schema_inference(tmp_path):
    # Create temporary sample CSV
    csv_file = tmp_path / "test_orders.csv"
    csv_file.write_text(
        "order_id,customer,amount,status\n"
        "1001,Alice,150.75,COMPLETED\n"
        "1002,Bob,89.00,PENDING\n"
        "1003,Charlie,210.50,COMPLETED\n"
    )

    df = IngestionExtractor.extract_file(str(csv_file), "CSV")
    assert isinstance(df, pl.DataFrame)
    assert df.height == 3
    assert "order_id" in df.columns

    schema_info = SchemaInferEngine.infer_schema_from_df(df)
    assert len(schema_info) == 4
    cols = {s["column_name"] for s in schema_info}
    assert cols == {"order_id", "customer", "amount", "status"}
