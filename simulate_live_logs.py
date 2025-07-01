import time

ioc_lines = [
    "mimikatz credential dumping", "powershell execution detected", "net user added",
    "cmd.exe started", "ftp session opened", "curl data exfiltration",
    "rundll32 suspicious call", "powershell encoded command",
    "cmd.exe /c whoami", "curl malicious.com"
    
]

with open("app/uploads/sysmon_realtime.log", "a") as f:
    for line in ioc_lines:
        f.write(line + "\n")
        print(f"[+] Injected: {line}")
        time.sleep(1)
