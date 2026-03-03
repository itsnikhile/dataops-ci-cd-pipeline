"""Great Expectations suite builder for automated data quality."""
import logging
from typing import Dict, List
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class ExpectationSuite:
    """Runs data quality expectations against a DataFrame."""
    def __init__(self, suite_name: str):
        self.name = suite_name
        self.results = []

    def expect_column_values_to_not_be_null(self, df, col):
        null_count = int(df[col].isna().sum()) if col in df.columns else len(df)
        passed = null_count == 0
        self.results.append({"expectation": f"not_null({col})", "passed": passed,
                              "unexpected_count": null_count, "severity": "error"})
        return passed

    def expect_column_values_to_be_unique(self, df, col):
        dupes = int(df[col].duplicated().sum()) if col in df.columns else 0
        passed = dupes == 0
        self.results.append({"expectation": f"unique({col})", "passed": passed,
                              "unexpected_count": dupes, "severity": "error"})
        return passed

    def expect_column_values_to_be_between(self, df, col, min_val, max_val):
        if col not in df.columns:
            self.results.append({"expectation": f"between({col})", "passed": False,
                                  "unexpected_count": len(df), "severity": "error"})
            return False
        out = int(((df[col] < min_val) | (df[col] > max_val)).sum())
        passed = out == 0
        self.results.append({"expectation": f"between({col},{min_val},{max_val})",
                              "passed": passed, "unexpected_count": out, "severity": "error"})
        return passed

    def expect_table_row_count_to_be_between(self, df, min_val, max_val=None):
        count = len(df)
        passed = count >= min_val and (max_val is None or count <= max_val)
        self.results.append({"expectation": f"row_count>={min_val}", "passed": passed,
                              "unexpected_count": 0 if passed else 1, "severity": "error"})
        return passed

    def expect_column_values_to_match_regex(self, df, col, pattern):
        if col not in df.columns:
            return False
        non_matching = int((~df[col].astype(str).str.match(pattern)).sum())
        passed = non_matching == 0
        self.results.append({"expectation": f"regex({col})", "passed": passed,
                              "unexpected_count": non_matching, "severity": "warning"})
        return passed

    def get_results(self):
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        failed = [r for r in self.results if not r["passed"]]
        return {"suite": self.name, "total": total, "passed": passed,
                "failed": len(failed), "success_rate": round(passed/total*100, 1) if total else 0,
                "failures": failed}
