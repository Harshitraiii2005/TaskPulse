from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from db import get_db_connection
from timezone_utils import ist_to_utc
from mailer import send_task_created_email, send_completion_email
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "taskpulse-secret")

# --- Home page / user signup ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        gender = request.form["gender"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id FROM users WHERE email=%s", (email,))
        user = cur.fetchone()

        if user:
            user_id = user[0]
        else:
            cur.execute("""
                INSERT INTO users (name, email, gender)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (name, email, gender))
            user_id = cur.fetchone()[0]
            conn.commit()

        cur.close()
        conn.close()
        return redirect(url_for("tasks", user_id=user_id))

    return render_template("index.html")

# --- Tasks page ---
@app.route("/tasks/<int:user_id>", methods=["GET", "POST"])
def tasks(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Add new task
    if request.method == "POST":
        title = request.form.get("title")
        due = request.form.get("due")
        if title and due:
            due_ist = datetime.fromisoformat(due)
            due_utc = ist_to_utc(due_ist)

            cur.execute("""
                INSERT INTO tasks (user_id, title, due_time, completed)
                VALUES (%s, %s, %s, FALSE)
            """, (user_id, title, due_utc))

            # Send task created email
            cur.execute("SELECT name, email FROM users WHERE id=%s", (user_id,))
            name, email = cur.fetchone()
            send_task_created_email(email, name, title, due_ist)

            conn.commit()

    # Fetch all tasks
    cur.execute("""
        SELECT id, title, due_time, completed
        FROM tasks
        WHERE user_id=%s
        ORDER BY completed ASC, due_time ASC
    """, (user_id,))
    db_tasks = cur.fetchall()

    # Format tasks for template: (id, title, formatted_due_date, completed)
    tasks = []
    for task in db_tasks:
        task_id, title, due_time, completed = task
        # Format due_time as readable string (YYYY-MM-DD HH:MM)
        try:
            formatted_due = due_time.strftime("%Y-%m-%d %H:%M") if due_time else "No date"
        except:
            formatted_due = str(due_time)
        tasks.append((task_id, title, formatted_due, completed))

    # Count incomplete tasks - if >= 10, no more can be added
    incomplete_tasks = [t for t in tasks if not t[3]]
    remaining_slots = max(0, 10 - len(incomplete_tasks))

    cur.close()
    conn.close()

    return render_template(
        "tasks.html",
        tasks=tasks,
        user_id=user_id,
        remaining_slots=remaining_slots
    )


# --- Complete a task ---
@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Mark task as completed instead of deleting
    cur.execute("""
        UPDATE tasks
        SET completed = TRUE
        WHERE id=%s
        RETURNING user_id, title
    """, (task_id,))
    task = cur.fetchone()

    if task:
        user_id, title = task
        # Get user info
        cur.execute("SELECT name, email FROM users WHERE id=%s", (user_id,))
        name, email = cur.fetchone()
        send_completion_email(email, name, title)
        conn.commit()
        cur.close()
        conn.close()
        # Redirect back to tasks page with user_id
        return redirect(url_for("tasks", user_id=user_id))

    cur.close()
    conn.close()
    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
