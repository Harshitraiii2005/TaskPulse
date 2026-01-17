import smtplib
import os
from email.message import EmailMessage


def send_completion_email(to_email, user_name, task_title):
    msg = EmailMessage()
    msg.set_content(f"""
 Congratulations {user_name}!

You have completed:
"{task_title}"

Keep it up 
– TaskPulse
""")
    msg["Subject"] = "Task Completed - TaskPulse"
    msg["From"] = os.getenv("EMAIL_ADDRESS")
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(
            os.getenv("EMAIL_ADDRESS"),
            os.getenv("EMAIL_APP_PASSWORD")
        )
        smtp.send_message(msg)
