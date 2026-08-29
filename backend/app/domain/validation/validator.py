from typing import Dict, Any, List
import polars as pl
from app.domain.validation.rules import QualityRule


class DataQualityValidator:
    """Run set of quality rules against dataset and compile quality report."""

    @staticmethod
    def run_validation(df: pl.DataFrame, rules_config: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_rules = len(rules_config)
        passed_rules = 0
        failed_rules = 0
        rules_summary = []

        for rule_cfg in rules_config:
            rule = QualityRule(
                rule_type=rule_cfg.get("rule_type", "NOT_NULL"),
                column=rule_cfg.get("column", ""),
                params=rule_cfg.get("params", {})
            )
            result = rule.evaluate(df)
            rules_summary.append(result)

            if result["passed"]:
                passed_rules += 1
            else:
                failed_rules += 1

        return {
            "total_rules": total_rules,
            "passed_rules": passed_rules,
            "failed_rules": failed_rules,
            "pass_rate_percentage": round((passed_rules / total_rules * 100), 2) if total_rules > 0 else 100.0,
            "rules_summary": rules_summary
        }
