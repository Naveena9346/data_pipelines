import re
from typing import Dict, Any, List
import polars as pl


class QualityRule:
    def __init__(self, rule_type: str, column: str, params: Dict[str, Any] = None):
        self.rule_type = rule_type
        self.column = column
        self.params = params or {}

    def evaluate(self, df: pl.DataFrame) -> Dict[str, Any]:
        if self.column not in df.columns:
            return {
                "rule": self.rule_type,
                "column": self.column,
                "passed": False,
                "message": f"Column '{self.column}' missing from dataset.",
                "failed_records": df.height
            }

        if self.rule_type == "NOT_NULL":
            null_count = df[self.column].null_count()
            passed = null_count == 0
            return {
                "rule": "NOT_NULL",
                "column": self.column,
                "passed": passed,
                "message": f"Found {null_count} null values." if not passed else "All values non-null.",
                "failed_records": null_count
            }

        elif self.rule_type == "UNIQUE":
            total_count = df.height
            unique_count = df[self.column].n_unique()
            duplicate_count = total_count - unique_count
            passed = duplicate_count == 0
            return {
                "rule": "UNIQUE",
                "column": self.column,
                "passed": passed,
                "message": f"Found {duplicate_count} duplicate entries." if not passed else "All values unique.",
                "failed_records": duplicate_count
            }

        elif self.rule_type == "VALUE_RANGE":
            min_val = self.params.get("min")
            max_val = self.params.get("max")
            col_series = df[self.column].cast(pl.Float64, strict=False)
            
            invalid_count = 0
            if min_val is not None:
                invalid_count += col_series.filter(col_series < float(min_val)).len()
            if max_val is not None:
                invalid_count += col_series.filter(col_series > float(max_val)).len()
                
            passed = invalid_count == 0
            return {
                "rule": "VALUE_RANGE",
                "column": self.column,
                "passed": passed,
                "message": f"Found {invalid_count} values outside range [{min_val}, {max_val}]." if not passed else "All values within range.",
                "failed_records": invalid_count
            }

        elif self.rule_type == "REGEX_MATCH":
            pattern = self.params.get("pattern", ".*")
            col_str = df[self.column].cast(pl.Utf8)
            invalid_count = col_str.filter(~col_str.str.contains(pattern)).len()
            passed = invalid_count == 0
            return {
                "rule": "REGEX_MATCH",
                "column": self.column,
                "passed": passed,
                "message": f"Found {invalid_count} values failing regex '{pattern}'." if not passed else "All values matched pattern.",
                "failed_records": invalid_count
            }

        else:
            return {
                "rule": self.rule_type,
                "column": self.column,
                "passed": True,
                "message": f"Unknown rule '{self.rule_type}' passed by default.",
                "failed_records": 0
            }
