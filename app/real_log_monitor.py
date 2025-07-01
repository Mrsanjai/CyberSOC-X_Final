# app/real_log_monitor.py

import json
import threading
import time
import os
from app.windows_log_reader import get_windows_logs  # ✅ Import your real log reader

def update_real_windows_logs():
    filepath = "realtime_windows_alerts.json"

    while True:
        try:
            # ✅ Get the 10 latest Security logs
            new_logs = get_windows_logs(log_type="Security", max_logs=10)

            # 🔄 Load existing logs (if file exists)
            if os.path.exists(filepath):
                try:
                    with open(filepath, "r") as f:
                        existing_logs = json.load(f)
                except:
                    existing_logs = []
            else:
                existing_logs = []

            # 🔁 Combine and keep latest 100 entries
            all_logs = existing_logs + new_logs
            all_logs = all_logs[-100:]

            # 💾 Write back to JSON file
            with open(filepath, "w") as f:
                json.dump(all_logs, f, indent=4)

        except Exception as e:
            print(f"[ERROR] Failed to update logs: {str(e)}")

        time.sleep(5)  # Refresh every 5 seconds

def start_real_log_monitor():
    t = threading.Thread(target=update_real_windows_logs)
    t.daemon = True
    t.start()
