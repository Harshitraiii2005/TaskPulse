import psycopg2
import os
from dotenv import load_dotenv
from backend.mailer import send_overdue_email

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

print("🔍 Checking overdue tasks...")

cur.execute("""
    SELECT t.id, t.title, t.due_time, u.email, u.name
    FROM tasks t
    JOIN users u ON t.user_id = u.id
    WHERE t.due_time <= NOW()
      AND (t.last_notified IS NULL
           OR t.last_notified <= NOW() - INTERVAL '1 hour')
""")

tasks = cur.fetchall()

for task_id, title, due_time, email, name in tasks:
    send_overdue_email(email, name, title, due_time)
    cur.execute(
        "UPDATE tasks SET last_notified = NOW() WHERE id=%s",
        (task_id,)
    )

conn.commit()
cur.close()
conn.close()

print(f"✅ Notifications sent: {len(tasks)}")
