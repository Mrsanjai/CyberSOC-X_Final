import json
from collections import Counter
from datetime import datetime

ALERTS_FILE = "alerts.json"

def load_alerts():
    try:
        with open(ALERTS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def get_alert_counts():
    alerts = load_alerts()
    status_counts = Counter(alert["status"] for alert in alerts)
    return dict(status_counts)

def get_alert_summary():
    alerts = load_alerts()
    summary = {
        "total_alerts": len(alerts),
        "by_source": Counter(alert["source"] for alert in alerts),
        "by_ioc": Counter(alert["ioc"] for alert in alerts),
        "recent": sorted(alerts, key=lambda x: x.get("timestamp", ""), reverse=True)[:10]
    }
    return summary

def filter_alerts_by_status(status):
    return [a for a in load_alerts() if a.get("status") == status]

def get_alert_by_id(alert_id):
    for alert in load_alerts():
        if alert["id"] == alert_id:
            return alert
    return None
