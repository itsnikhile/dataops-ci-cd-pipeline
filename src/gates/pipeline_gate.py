"""CI/CD quality gate — blocks or allows pipeline progression."""
import logging
from typing import Dict, List
from src.quality.expectation_suite import ExpectationSuite
import pandas as pd

logger = logging.getLogger(__name__)

class PipelineGate:
    """Evaluates quality gates and determines if deployment should proceed."""

    def __init__(self, min_success_rate: float = 100.0, allow_warnings: bool = True):
        self.min_success_rate = min_success_rate
        self.allow_warnings = allow_warnings

    def build_suite(self, suite_name: str, df: pd.DataFrame) -> ExpectationSuite:
        suite = ExpectationSuite(suite_name)
        suite.expect_table_row_count_to_be_between(df, 1000)
        for col in ["user_id", "transaction_id", "created_at"]:
            if col in df.columns:
                suite.expect_column_values_to_not_be_null(df, col)
        if "transaction_id" in df.columns:
            suite.expect_column_values_to_be_unique(df, "transaction_id")
        if "amount" in df.columns:
            suite.expect_column_values_to_be_between(df, "amount", 0.01, 1_000_000)
        if "email" in df.columns:
            suite.expect_column_values_to_match_regex(df, "email", r".+@.+\..+")
        return suite

    def evaluate(self, df: pd.DataFrame, suite_name: str) -> Dict:
        suite = self.build_suite(suite_name, df)
        results = suite.get_results()
        errors = [f for f in results["failures"] if f.get("severity") == "error"]
        warnings = [f for f in results["failures"] if f.get("severity") == "warning"]

        gate_passed = (results["success_rate"] >= self.min_success_rate or
                       (self.allow_warnings and len(errors) == 0))

        logger.info(f"Gate [{suite_name}]: {'PASS' if gate_passed else 'BLOCK'} | "
                    f"{results['passed']}/{results['total']} checks | "
                    f"{len(errors)} errors | {len(warnings)} warnings")

        return {**results, "gate_passed": gate_passed,
                "errors": len(errors), "warnings": len(warnings)}
