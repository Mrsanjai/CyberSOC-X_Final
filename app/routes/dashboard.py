from flask import Blueprint, render_template, redirect, url_for, jsonify, flash, request
from flask_login import login_required, current_user
from app.routes.alert_utils import get_alert_summary, get_alert_counts, load_alerts
from collections import defaultdict
from datetime import datetime
import os

dashboard_bp = Blueprint("dashboard", __name__)

# ⛳ Redirect root to /dashboard
@dashboard_bp.route("/")
def index():
    return redirect(url_for("dashboard.dashboard"))

# 🧠 Main Dashboard View
@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    summary = get_alert_summary()
    status_counts = get_alert_counts()
    total_alerts = summary.get("total_alerts", 0)

    return render_template("dashboard.html",
                           user=current_user,
                           total_alerts=total_alerts,
                           status_counts=status_counts)

# 📊 Alert counts by status + source
@dashboard_bp.route("/dashboard/summary")
def dashboard_summary():
    summary = get_alert_summary()
    summary["status_counts"] = get_alert_counts()
    return jsonify(summary)

# 📊 📈 Timeline trend data for graph (NEW)
@dashboard_bp.route("/dashboard/timeline")
def alert_timeline():
    alerts = load_alerts()
    timeline = defaultdict(int)

    for alert in alerts:
        ts = alert.get("timestamp")
        if ts:
            try:
                dt = datetime.fromisoformat(ts)
                key = dt.strftime("%Y-%m-%d")
                timeline[key] += 1
            except Exception:
                continue

    # Sorted by date ascending
    sorted_data = sorted(timeline.items())
    labels = [d[0] for d in sorted_data]
    values = [d[1] for d in sorted_data]

    return jsonify({"labels": labels, "values": values})

# 🔔 Header Alert Poll
@dashboard_bp.route("/dashboard/notifications")
def get_new_alerts():
    alerts = load_alerts()
    new_alerts = [a for a in alerts if a.get("status") == "new" and a.get("source") == "RealTimeMonitor"]
    return jsonify({"count": len(new_alerts), "alerts": new_alerts[-3:]})

# 🔁 Toast Stream
@dashboard_bp.route("/dashboard/stream")
def alert_stream():
    alerts = load_alerts()
    realtime_alerts = [a for a in alerts if a.get("source") == "RealTimeMonitor" and a.get("status") == "new"]
    return jsonify(realtime_alerts[-1] if realtime_alerts else {})

# 🧹 Reset Logs
@dashboard_bp.route("/dashboard/reset-logs", methods=["POST"])
@login_required
def reset_logs():
    try:
        for file in ["alerts.json", "app/data/realtime_windows_alerts.json", "app/uploads/sysmon_realtime.log"]:
            with open(file, "w") as f:
                f.write("[]" if file.endswith(".json") else "")
        return jsonify({"success": True, "message": "Logs have been reset."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
