import json
from datetime import datetime

alert = {
    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "ioc": "Manual Test",
    "summary": "[TEST] Manual test alert for Real-Time Windows Monitoring"
}

with open("app/data/realtime_windows_alerts.json", "r+") as f:
    data = json.load(f)
    data.insert(0, alert)
    f.seek(0)
    json.dump(data, f, indent=2)
    f.truncate()
