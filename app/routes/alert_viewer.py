from flask import Blueprint, render_template, request
from flask_login import login_required
from app.routes.alert_utils import load_alerts
import json

alerts_bp = Blueprint("alerts", __name__)

@alerts_bp.route("/alerts", methods=["GET"])
@login_required
def view_alerts():
    status_filter = request.args.get("status")
    keyword_filter = request.args.get("keyword", "").lower()

    try:
        alerts = load_alerts()
    except (FileNotFoundError, json.JSONDecodeError):
        alerts = []

    if status_filter:
        alerts = [a for a in alerts if a["status"] == status_filter]
    if keyword_filter:
        alerts = [a for a in alerts if keyword_filter in a["ioc"].lower() or keyword_filter in a["summary"].lower()]

    alerts = sorted(alerts, key=lambda x: x.get("timestamp", ""), reverse=True)
    return render_template("alerts.html", alerts=alerts)
