# Export Sysmon logs to a file in real-time
$logPath = "F:\project\CyberSOC-X_Final\app\uploads\sysmon_realtime.log"

while ($true) {
    Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" -MaxEvents 5 |
    ForEach-Object {
        $_.Message | Out-File -Append $logPath
    }
    Start-Sleep -Seconds 5
}
