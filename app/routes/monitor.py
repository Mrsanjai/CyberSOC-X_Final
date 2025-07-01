# app/routes/monitor.py

from flask import Blueprint, render_template
import json
import os
from datetime import datetime

monitor_bp = Blueprint('winlog', __name__)


# Add this to monitor.py
@monitor_bp.route("/api/logs")
def api_logs():
    filepath = "realtime_windows_alerts.json"
    try:
        with open(filepath, "r") as f:
            logs = json.load(f)
        logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return {"logs": logs[:10]}
    except Exception as e:
        return {"error": str(e)}, 500


# app/routes/monitor.py

@monitor_bp.route("/")
def home():
    filepath = "realtime_windows_alerts.json"

    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            json.dump([], f)

    try:
        with open(filepath, "r") as f:
            logs = json.load(f)

        logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        logs = logs[:10]  # latest 10

        # Enhance display
        for log in logs:
            # Pretty time
            try:
                dt = datetime.fromisoformat(log.get("timestamp", ""))
                log["pretty_time"] = dt.strftime("%a %b %d %H:%M:%S %Y")
            except:
                log["pretty_time"] = log.get("timestamp", "")

            # Clean up message
            msg = log.get("message", "")
            if isinstance(msg, list):
                msg = " | ".join(str(m).replace("\r", "").replace("\n", " ").replace("\t", "").strip() for m in msg)
            elif isinstance(msg, str):
                msg = msg.replace("\r", "").replace("\n", " ").replace("\t", "").strip()
            log["message"] = msg

    except Exception as e:
        logs = [{"error": f"Failed to load logs: {str(e)}"}]

    return render_template("windows_logs.html", logs=logs)
