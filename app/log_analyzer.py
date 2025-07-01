# app/log_analyzer.py

def analyze_log_line(line):
    line = line.lower()
    
    if "logon failure" in line or "failed login" in line or "4625" in line:
        return "high", "Failed Login Attempt"
    
    elif "powershell" in line or "cmd.exe" in line or "wscript" in line:
        return "high", "Suspicious Scripting"

    elif "usb device" in line or "drive mounted" in line:
        return "medium", "USB Device Activity"

    elif "firewall" in line or "blocked connection" in line:
        return "medium", "Firewall Event"

    elif "service crashed" in line or "unexpected shutdown" in line:
        return "medium", "System Instability"

    else:
        return "low", "General Log Activity"
