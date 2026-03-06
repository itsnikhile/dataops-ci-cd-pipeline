import pandas as pd
import numpy as np
import json
import os

np.random.seed(42)
n = 50000
df = pd.DataFrame({
    "transaction_id": ["TXN_{:08d}".format(i) for i in range(n)],
    "user_id": ["USER_{:05d}".format(np.random.randint(0, 10000)) for _ in range(n)],
    "amount": np.random.lognormal(4, 1, n).round(2),
    "email": ["u{}@example.com".format(i) for i in range(n)],
})

checks = {
    "row_count":       len(df) >= 1000,
    "no_null_user_id": df["user_id"].isna().sum() == 0,
    "no_null_txn_id":  df["transaction_id"].isna().sum() == 0,
    "unique_txn_ids":  df["transaction_id"].duplicated().sum() == 0,
    "valid_amounts":   bool(((df["amount"] > 0) & (df["amount"] < 1000000)).all()),
}

passed = sum(checks.values())
total  = len(checks)
rate   = round(passed / total * 100, 1)

print("Quality Gate Results:")
for name, result in checks.items():
    status = "PASS" if result else "FAIL"
    print("  {} - {}".format(status, name))
print("Score: {}/{} ({}%)".format(passed, total, rate))

os.makedirs("reports", exist_ok=True)
with open("reports/quality_report.json", "w") as f:
    json.dump({"passed": passed, "total": total, "rate": rate, "checks": checks}, f, indent=2)

if passed < total:
    print("Gate BLOCKED")
    raise SystemExit(1)

print("Gate PASSED")
