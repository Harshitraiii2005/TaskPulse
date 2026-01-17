import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from backend.timezone_utils import utc_to_ist

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

def _send(msg):
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        # Log the failure but don’t crash Flask
        print("❌ Failed to send email:", e)

def send_task_created_email(email, name, title, due_ist):
    msg = EmailMessage()
    msg.set_content(f"""
Hi {name},

📝 New task added to TaskPulse

Task: {title}
Due: {due_ist.strftime('%d %b %Y, %I:%M %p')} (IST)

We’ll remind you if it’s overdue ⏰

– TaskPulse
""")
    msg["Subject"] = "📝 Task Added"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email
    _send(msg)

def send_completion_email(email, name, title):
    msg = EmailMessage()
    msg.set_content(f"""
Hi {name},

🎉 Congratulations!

You completed:
✅ {title}

Keep going 💪🔥

– TaskPulse
""")
    msg["Subject"] = "🎉 Task Completed"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email
    _send(msg)

def send_overdue_email(email, name, title, due_utc):
    due_ist = utc_to_ist(due_utc)
    msg = EmailMessage()
    msg.set_content(f"""
Hi {name},

 Task Overdue Reminder

Task: {title}
Due: {due_ist.strftime('%d %b %Y, %I:%M %p')} (IST)

Please complete it soon.

– TaskPulse
""")
    msg["Subject"] = f" Overdue: {title}"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email
    _send(msg)
