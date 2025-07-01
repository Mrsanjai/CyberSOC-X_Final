# simulate_log.py

import time

# This path must match the one in your log_monitor.py
log_path = "app/uploads/sysmon_realtime.log"

ioc_lines = [
    "[INFO] Normal startup event",
    "[WARNING] Unusual process behavior",
    "[ALERT] Suspicious PowerShell encodedcommand detected",
    "[CRITICAL] mimikatz activity detected from user shell",
    "[INFO] Health check passed",
    "[WARNING] Nmap scan initiated on port range",
    "[INFO] Terminating monitoring session"
]

def simulate_logs():
    print(f"🧪 Writing test logs to: {log_path}")
    with open(log_path, "a") as f:
        for line in ioc_lines:
            f.write(line + "\n")
            print(f"→ Logged: {line}")
            time.sleep(2)

if __name__ == "__main__":
    simulate_logs()
