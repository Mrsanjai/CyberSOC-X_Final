from app import create_app

import subprocess
import os

# Start PowerShell script in background
powershell_script_path = r"F:\project\CyberSOC-X_Final\sysmon_export.ps1"
subprocess.Popen(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", powershell_script_path])

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
