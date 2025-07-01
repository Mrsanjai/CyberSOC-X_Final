# 🛡️ CyberSOC-X Final

A professional-grade real-time cybersecurity dashboard and log analyzer built in Flask.  
It simulates a SOC/XDR system with live alerts, log upload analyzers, role-based login with MFA, training simulations, and system health monitoring.

---

## 🔧 Features
- ✅ User login + MFA (TOTP/email)
- ✅ Role-based access (Admin, Analyst, Responder)
- ✅ Real-time Sysmon + PCAP analysis
- ✅ Live alert engine (`alerts.json`)
- ✅ Dashboard with chart.js graphs
- ✅ IR console: escalate, contain, close
- ✅ Training simulator: fake red/blue team alerts
- ✅ System monitor (CPU, RAM via psutil)

---

## 🚀 How to Run

1. Install requirements:
   ```bash
   pip install -r requirements.txt
