"""Background job entry points for scanner and alert scheduling.
Wire these into Celery/RQ/Arq in production.
"""

from app.services.scanner import ScannerService


def run_market_scan(strategy: dict) -> dict:
    scanner = ScannerService()
    return scanner.scan(strategy).model_dump()


def emit_alerts(scan_result: dict) -> list[dict]:
    alerts: list[dict] = []
    for setup in scan_result.get("setups", []):
        if setup["final_action"] in {"EXECUTE", "PLACE_LIMIT_ORDER"}:
            alerts.append({"type": "SETUP", "market": setup["market"], "action": setup["final_action"]})
        if setup["event_risk_status"] == "DO_NOT_ENTER_BEFORE_NEWS":
            alerts.append({"type": "EVENT_RISK", "market": setup["market"]})
    return alerts
