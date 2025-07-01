from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app.routes.alert_utils import load_alerts
import psutil
import datetime

monitor_bp = Blueprint('system_monitor', __name__)

# 📊 System Performance Monitor Page
@monitor_bp.route("/monitor")
@login_required
def monitor():
    return render_template("monitor.html")

# 🌐 Real-time System Metrics Endpoint (AJAX)
@monitor_bp.route("/monitor/data")
@login_required
def monitor_data():
    data = {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "net_sent": round(psutil.net_io_counters().bytes_sent / 1024 / 1024, 2),
        "net_recv": round(psutil.net_io_counters().bytes_recv / 1024 / 1024, 2),
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
    }
    return jsonify(data)

# 🧠 Windows Event Log Monitor Page
@monitor_bp.route("/win-monitor")
@login_required
def win_monitor():
    alerts = load_alerts()
    windows_alerts = [a for a in alerts if a.get("source", "").startswith("WinEvent")]
    return render_template("win_monitor.html", alerts=windows_alerts)
