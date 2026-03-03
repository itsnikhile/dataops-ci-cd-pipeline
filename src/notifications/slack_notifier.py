"""Slack notifications for pipeline gate results."""
import os, logging, requests
from datetime import datetime
from typing import Dict

logger = logging.getLogger(__name__)
WEBHOOK = os.getenv("SLACK_WEBHOOK_URL", "")

class SlackNotifier:
    def __init__(self, webhook: str = WEBHOOK):
        self.webhook = webhook

    def notify_gate_result(self, gate_result: Dict, pipeline: str, env: str = "prod"):
        passed = gate_result.get("gate_passed", False)
        color = "good" if passed else "danger"
        icon = "✅" if passed else "🚨"
        msg = {
            "attachments": [{
                "color": color,
                "title": f"{icon} DataOps Gate: {'PASSED' if passed else 'BLOCKED'}",
                "text": f"*Pipeline:* `{pipeline}` | *Env:* `{env}` | *Time:* {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
                "fields": [
                    {"title": "Total Checks", "value": str(gate_result.get("total", 0)), "short": True},
                    {"title": "Passed",        "value": str(gate_result.get("passed", 0)), "short": True},
                    {"title": "Errors",        "value": str(gate_result.get("errors", 0)), "short": True},
                    {"title": "Warnings",      "value": str(gate_result.get("warnings", 0)), "short": True},
                ],
            }]
        }
        if self.webhook:
            try:
                requests.post(self.webhook, json=msg, timeout=5)
            except Exception as e:
                logger.warning(f"Slack send failed: {e}")
        else:
            logger.info(f"[SLACK] {icon} {pipeline} gate {'PASSED' if passed else 'BLOCKED'} "
                        f"({gate_result.get('passed')}/{gate_result.get('total')} checks)")
