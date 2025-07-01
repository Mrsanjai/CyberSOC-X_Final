from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
import json
from datetime import datetime
from scapy.all import rdpcap, TCP, UDP, IP

pcap_bp = Blueprint("pcap", __name__)

UPLOAD_FOLDER = "app/uploads"

@pcap_bp.route("/pcap", methods=["GET", "POST"])
def pcap_upload():
    alerts = []

    if request.method == "POST":
        file = request.files.get("pcapfile")
        if file and file.filename.endswith(".pcap"):
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            try:
                packets = rdpcap(filepath)
                for i, pkt in enumerate(packets):
                    if IP in pkt:
                        ip_src = pkt[IP].src
                        ip_dst = pkt[IP].dst
                        proto = "TCP" if TCP in pkt else "UDP" if UDP in pkt else "OTHER"
                        flags = str(pkt[TCP].flags) if TCP in pkt else ""

                        # IOC: Port scan behavior (many TCP SYNs)
                        if TCP in pkt and flags == "S":
                            alerts.append({
                                "id": f"pcap-{i}",
                                "source": "PCAP",
                                "ioc": "TCP SYN Scan (possible Nmap)",
                                "timestamp": datetime.utcnow().isoformat(),
                                "summary": f"Suspicious scan from {ip_src} to {ip_dst}",
                                "status": "new"
                            })
            except Exception as e:
                flash(f"Error parsing PCAP: {str(e)}", "danger")
                return redirect(url_for("pcap.pcap_upload"))

            # Save alerts
            if alerts:
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
            return redirect(url_for("pcap.pcap_upload"))
        else:
            flash("Invalid file type. Only .pcap allowed.", "danger")

    return render_template("pcap_upload.html")
