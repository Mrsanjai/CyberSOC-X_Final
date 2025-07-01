from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
import json
from datetime import datetime

# Blueprint for Sysmon upload
sysmon_bp = Blueprint('sysmon', __name__)

UPLOAD_FOLDER = "app/uploads"
IOC_KEYWORDS = ["powershell", "mimikatz", "nmap", "rundll32", "encodedcommand", "cmd /c", "reg add", "schtasks"]

@sysmon_bp.route("/sysmon", methods=["GET", "POST"])
def sysmon():
    alerts = []

    if request.method == "POST":
        file = request.files.get("logfile")
        if file and file.filename:
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists
            file.save(filepath)

            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                for keyword in IOC_KEYWORDS:
                    if keyword.lower() in line.lower():
                        alert = {
                            "id": f"sysmon-{i}",
                            "source": "Sysmon",
                            "ioc": keyword,
                            "timestamp": datetime.utcnow().isoformat(),
                            "summary": f"IOC '{keyword}' detected in line {i+1} of {filename}",
                            "status": "new"
                        }
                        alerts.append(alert)

            # Save alerts to alerts.json
            try:
                with open("alerts.json", "r+") as f:
                    try:
                        existing_alerts = json.load(f)
                    except json.JSONDecodeError:
                        existing_alerts = []
                    existing_alerts.extend(alerts)
                    f.seek(0)
                    json.dump(existing_alerts, f, indent=4)
                    f.truncate()
            except FileNotFoundError:
                with open("alerts.json", "w") as f:
                    json.dump(alerts, f, indent=4)

            flash(f"Uploaded and parsed {filename}. {len(alerts)} alert(s) generated.", "success")
            return redirect(url_for("sysmon.sysmon"))
        else:
            flash("No file selected.", "danger")

    return render_template("sysmon.html")
