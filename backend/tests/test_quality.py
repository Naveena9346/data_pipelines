import pytest
import polars as pl
from app.domain.validation.validator import DataQualityValidator


def test_data_quality_rules_validation():
    df = pl.DataFrame({
        "email": ["user1@test.com", "user2@test.com", None],
        "age": [25, 40, 150],
        "account_id": ["A1", "A2", "A1"]
    })

    rules_config = [
        {"rule_type": "NOT_NULL", "column": "email"},
        {"rule_type": "VALUE_RANGE", "column": "age", "params": {"min": 0, "max": 120}},
        {"rule_type": "UNIQUE", "column": "account_id"}
    ]

    report = DataQualityValidator.run_validation(df, rules_config)
    assert report["total_rules"] == 3
    assert report["failed_rules"] == 3
    assert report["passed_rules"] == 0

    # Clean dataset test
    clean_df = pl.DataFrame({
        "email": ["user1@test.com", "user2@test.com", "user3@test.com"],
        "age": [25, 40, 30],
        "account_id": ["A1", "A2", "A3"]
    })
    clean_report = DataQualityValidator.run_validation(clean_df, rules_config)
    assert clean_report["passed_rules"] == 3
    assert clean_report["failed_rules"] == 0
    assert clean_report["pass_rate_percentage"] == 100.0
