"""DataOps CI/CD Pipeline — Quality Gate Runner"""
import sys, logging, json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def generate_data(n=50000, inject_issues=False):
    np.random.seed(42)
    df = pd.DataFrame({
        "transaction_id": [f"TXN_{i:08d}" for i in range(n)],
        "user_id": [f"USER_{np.random.randint(0,10000):05d}" for _ in range(n)],
        "amount": np.random.lognormal(4, 1, n).round(2),
        "email": [f"u{i}@example.com" for i in range(n)],
        "created_at": [datetime.utcnow() - timedelta(hours=np.random.uniform(0, 20)) for _ in range(n)],
    })
    if inject_issues:
        df.loc[:50, "user_id"] = None
        df.loc[51:100, "amount"] = -999
    return df

def run_gate(env="staging"):
    from src.gates.pipeline_gate import PipelineGate
    from src.notifications.slack_notifier import SlackNotifier
    gate = PipelineGate()
    notifier = SlackNotifier()
    df = generate_data(50000, inject_issues=(env == "demo-bad"))
    result = gate.evaluate(df, "transactions_pipeline")
    notifier.notify_gate_result(result, "transactions-pipeline", env)
    import os
    os.makedirs("reports", exist_ok=True)
    with open("reports/quality_report.json", "w") as f:
        json.dump(result, f, indent=2, default=str)
    logger.info(f"Gate result: {'PASSED' if result['gate_passed'] else 'BLOCKED'}")
    return result["gate_passed"]

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "gate"
    env  = sys.argv[2].replace("--env=","").replace("--env ","") if len(sys.argv) > 2 else "staging"
    if mode == "gate":
        passed = run_gate(env)
        sys.exit(0 if passed else 1)
