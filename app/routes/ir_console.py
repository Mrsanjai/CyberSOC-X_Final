from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required
from app.routes.alert_utils import load_alerts
import pdfkit
import json
from datetime import datetime
import csv
import io

ir_bp = Blueprint("ir_console", __name__)
REMEDIATION_LOG = "remediation_log.json"

# ✅ IR Console Page (GET)
@ir_bp.route("/ir-console", methods=["GET"])
@login_required
def ir_console():
    status_filter = request.args.get("status")
    keyword_filter = request.args.get("keyword", "").lower()

    try:
        alerts = load_alerts()
    except (FileNotFoundError, json.JSONDecodeError):
        alerts = []

    # Filters
    if status_filter:
        alerts = [a for a in alerts if a.get("status") == status_filter]

    if keyword_filter:
        alerts = [a for a in alerts if keyword_filter in a.get("ioc", "").lower() or keyword_filter in a.get("summary", "").lower()]

    alerts = sorted(alerts, key=lambda x: x.get("timestamp", ""), reverse=True)
    return render_template("ir_console.html", alerts=alerts)

# ✅ Handle Status Update & Remediation Actions (POST)
@ir_bp.route("/ir-console", methods=["POST"])
@login_required
def update_alert_status():
    try:
        with open("alerts.json", "r") as f:
            alerts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        alerts = []

    action = request.form.get("action")
    alert_id = request.form.get("alert_id")

    updated = False
    remediation_action = None

    for alert in alerts:
        if alert["id"] == alert_id:
            if action in ["escalated", "closed"]:
                alert["status"] = action
                alert["last_updated"] = datetime.utcnow().isoformat()
                updated = True
            elif action.startswith("remediate_"):
                remediation_action = {
                    "id": alert_id,
                    "ioc": alert.get("ioc", ""),
                    "action": action.replace("remediate_", ""),
                    "analyst": "admin",  # Replace with current_user.username if using real login
                    "timestamp": datetime.utcnow().isoformat()
                }
                break

    if updated:
        with open("alerts.json", "w") as f:
            json.dump(alerts, f, indent=4)
        flash(f"✅ Alert {alert_id} marked as {action}.", "success")

    if remediation_action:
        try:
            with open(REMEDIATION_LOG, "r") as f:
                rem_logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            rem_logs = []

        rem_logs.append(remediation_action)
        with open(REMEDIATION_LOG, "w") as f:
            json.dump(rem_logs, f, indent=4)
        flash(f"🛡️ Remediation '{remediation_action['action']}' logged for alert {alert_id}.", "info")

    return redirect(url_for("ir_console.ir_console"))

# ✅ Export to CSV
@ir_bp.route("/ir-console/export/csv")
@login_required
def export_alerts_csv():
    alerts = load_alerts()
    output = io.StringIO()
    fieldnames = ["id", "ioc", "summary", "status", "timestamp", "source", "severity", "mitre_tactic", "mitre_technique", "last_updated"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for alert in alerts:
        for key in fieldnames:
            if key not in alert:
                alert[key] = ""
        writer.writerow(alert)
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment; filename=alerts.csv"}
    )

# ✅ Export to PDF (HTML Template → PDF)
@ir_bp.route("/ir-console/export/pdf")
@login_required
def export_alerts_pdf():
    alerts = load_alerts()
    rendered = render_template("export_pdf_template.html", alerts=alerts)

    try:
        # If wkhtmltopdf is not on PATH, configure path manually here
        # config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        # pdf = pdfkit.from_string(rendered, False, configuration=config)

        pdf = pdfkit.from_string(rendered, False)
        return Response(
            pdf,
            mimetype='application/pdf',
            headers={"Content-Disposition": "attachment; filename=alerts.pdf"}
        )
    except Exception as e:
        return f"❌ PDF generation failed: {str(e)}", 500
