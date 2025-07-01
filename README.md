# 🛡️ CyberSOC-X_Final — AI-Powered SOC Dashboard

A powerful **Security Operations Center (SOC) Dashboard** built using Flask, integrating real-time alerting, log monitoring, threat detection, and incident response capabilities.

> 🔐 Developed by [Sanjai M](https://github.com/Mrsanjai)  
> 🎯 Target Role: SOC Analyst | Blue Team | Threat Hunter

---

## 🚀 Features

- 🧠 **Real-Time Log Monitoring** (Sysmon, Windows Event Logs)
- 📤 **Upload & Analyze Logs/PCAPs**
- 🚨 **Alert Classification:** New, Escalated, Closed
- 🔎 **IOC Detection Engine** (Mimikatz, Powershell, RDP Brute, etc.)
- 📁 **Export Reports:** PDF & CSV
- 🧪 **APT Simulation Training Lab**
- ⚠️ **Slack Notifications for Critical Alerts**
- 💬 **IR Console with Search, Filters & Action Buttons (Block IP, Quarantine, etc.)**
- 🌑 **Oculux-Inspired Dark Themed UI (Modern + Responsive)**

---

## 📸 Screenshots

> Create a folder named `screenshots/` and upload your images. Add image links like below:

| Dashboard | Real-time Alerts | Incident Console |
|----------|------------------|------------------|
| ![Dashboard](screenshots/dashboard.png) | ![Alerts](screenshots/alerts.png) | ![IR Console](screenshots/ir_console.png) |

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JS, Bootstrap
- **Monitoring**: Sysmon, PowerShell, Slack Webhook
- **Export**: WeasyPrint (PDF), CSV
- **UI**: Dark Theme (Oculux Inspired)

---


---

## 🔧 Setup Instructions

bash
# Clone the repo
git clone https://github.com/Mrsanjai/CyberSOC-X_Final.git
cd CyberSOC-X_Final

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python run.py

🎓 Project Purpose
This project was developed as a final showcase for SOC skill development, combining automation, detection, and professional dashboard design to simulate real-world analyst scenarios.

🔖 Tags
#SOC #SIEM #CyberSecurity #IncidentResponse #Python #Snort #Sysmon #Flask

🙋‍♂️ Author
Sanjai R
💼 Cybersecurity Mentor 
🔗 GitHub: Mrsanjai
📧 Email: sanjai.blackheart@gmail.com

dashboard
![image](https://github.com/user-attachments/assets/062ddebf-023e-434d-bc64-befc90ff14f0)
Sysmon Log File
![image](https://github.com/user-attachments/assets/cc37ef9a-5b8b-4d43-967d-ca537d5bb122)
Upload Network Capture 
![image](https://github.com/user-attachments/assets/92f752b6-50e7-456a-864e-a8521a0a416d)
APT Simulation Lab
![image](https://github.com/user-attachments/assets/eabc5bd6-391c-419a-9f34-4cd176706f21)
Incident Response Console
![image](https://github.com/user-attachments/assets/66825aa0-bc57-4150-8b76-a23a4749a67f)
Alert Console
![image](https://github.com/user-attachments/assets/f2ee3401-aae4-474b-bce9-bce8a87301ef)
Live Windows Event Logs
![image](https://github.com/user-attachments/assets/6178289d-88d2-4a9a-b111-124d9614f78c)
System Resource Monitor
![image](https://github.com/user-attachments/assets/bcefda63-d14c-4bbf-b0f7-c394f1997786)
Reset
![image](https://github.com/user-attachments/assets/7bee954f-2a7d-4348-8647-06b7644b27f5)


git add screenshots/
git commit -m "📸 Added screenshots for README"
git push origin main


Note: run VS Code as an admin !!

