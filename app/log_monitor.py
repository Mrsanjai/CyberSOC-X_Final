import threading, time, json, os
from datetime import datetime
from app.notifier import send_alert_to_all
from app.anomaly_detector import AnomalyDetector

anomaly_detector = AnomalyDetector()

IOC_MITRE_MAP = {
    "mimikatz":   ("Credential Access", "T1003.001", "high"),
    "powershell": ("Execution",         "T1059.001", "medium"),
    "net user":   ("Discovery",         "T1087.001", "medium"),
    "rundll32":   ("Execution",         "T1218.011", "high"),
    "cmd.exe":    ("Execution",         "T1059.003", "medium"),
    "ftp":        ("Command and Control", "T1105",   "high"),
    "curl":       ("Command and Control", "T1105",   "medium")
}

ALERTS_FILE = "alerts.json"
REALTIME_ALERTS_FILE = "app/data/realtime_windows_alerts.json"
LOG_FILE = "app/uploads/sysmon_realtime.log"

def add_to_realtime_alerts(alert):
    alert_entry = {
        "timestamp": alert["timestamp"],
        "ioc": alert["ioc"],
        "summary": alert["summary"],
        "mitre_tactic": alert.get("mitre_tactic", "Unknown"),
        "mitre_technique": alert.get("mitre_technique", "N/A"),
        "severity": alert.get("severity", "medium")
    }
    try:
        with open(REALTIME_ALERTS_FILE, "r+") as f:
            data = json.load(f)
            data.insert(0, alert_entry)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
    except (FileNotFoundError, json.JSONDecodeError):
        with open(REALTIME_ALERTS_FILE, "w") as f:
            json.dump([alert_entry], f, indent=2)

def save_alert(alert):
    try:
        with open(ALERTS_FILE, "r+") as f:
            alerts = json.load(f)
            alerts.append(alert)
            f.seek(0)
            json.dump(alerts, f, indent=4)
            f.truncate()
    except (FileNotFoundError, json.JSONDecodeError):
        with open(ALERTS_FILE, "w") as f:
            json.dump([alert], f, indent=4)

def process_ioc_detection(line):
    for keyword, (tactic, technique, severity) in IOC_MITRE_MAP.items():
        if keyword.lower() in line.lower():
            summary = f"⚠️ Detected '{keyword}' in live log stream"
            alert = {
                "id": f"rt-{int(time.time())}",
                "source": "RealTimeMonitor",  # ✅ Must be here for dashboard graph
                "ioc": keyword,
                "timestamp": datetime.utcnow().isoformat(),
                "summary": summary,
                "status": "new",
                "severity": severity,
                "mitre_tactic": tactic,
                "mitre_technique": technique
            }

            print(f"[ALERT] {summary}")
            save_alert(alert)
            add_to_realtime_alerts(alert)

            full_msg = f"🚨 *{tactic} ({technique})*\nIOC: `{keyword}`\nSummary: {summary}"
            send_alert_to_all(full_msg)
            break

def process_ml_detection(line):
    if anomaly_detector.is_anomalous(line):
        summary = f"🤖 ML Anomaly Detected: {line[:80]}..."
        alert = {
            "id": f"ml-{int(time.time())}",
            "source": "AnomalyDetector",
            "ioc": "anomaly",
            "timestamp": datetime.utcnow().isoformat(),
            "summary": summary,
            "status": "new",
            "severity": "high",
            "mitre_tactic": "Unknown",
            "mitre_technique": "N/A"
        }

        print(f"[ML ALERT] {summary}")
        save_alert(alert)
        add_to_realtime_alerts(alert)
        send_alert_to_all(summary)

def process_line(line):
    process_ioc_detection(line)
    process_ml_detection(line)

def train_anomaly_model():
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()[-300:]
        anomaly_detector.train(lines)
    except Exception as e:
        print(f"[ML] Training error: {e}")

def tail_log():
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, "w").close()

    train_anomaly_model()

    with open(LOG_FILE, "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line:
                process_line(line.strip())
            else:
                time.sleep(1)

def start_monitoring():
    t = threading.Thread(target=tail_log, daemon=True)
    t.start()
