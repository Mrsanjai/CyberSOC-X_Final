# app/notifier.py

import requests
import smtplib
from email.mime.text import MIMEText

# ========== 🔐 CONFIGURE THESE ==========

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"  # ✅ Your Slack webhook

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = " sdsanjai.blackheart@gmail.com"       # ✅ Your sender Gmail
EMAIL_PASSWORD = "hgzkpvxhchkarjeg"                # ✅ Gmail app password (App-specific, not your actual Gmail password)
EMAIL_RECEIVER = "sanjai.gozler@gmail.com"          # ✅ Receiver email

# ========================================


# ========== 📢 SLACK ALERT ==========

def send_slack_alert(message):
    if not SLACK_WEBHOOK_URL:
        print("⚠️ [Slack] Webhook URL not configured. Skipping alert.")
        return

    try:
        payload = {"text": f"🚨 *CyberSOC-X Alert:* {message}"}
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)

        if response.status_code == 200:
            print("✅ [Slack] Alert sent successfully")
        else:
            print(f"❌ [Slack] Failed with code {response.status_code}: {response.text}")

    except Exception as e:
        print(f"❌ [Slack] Exception occurred: {e}")


# ========== 📧 EMAIL ALERT ==========

def send_email_alert(subject, message):
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        print("✅ [Email] Alert sent successfully")

    except Exception as e:
        print(f"❌ [Email] Error: {e}")


# ========== 🔔 COMBINED ALERT CALL ==========

def send_alert_to_all(message):
    send_slack_alert(message)
    send_email_alert("🚨 CyberSOC-X Alert", message)
