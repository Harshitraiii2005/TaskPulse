from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from backend.db import get_db_connection
from backend.timezone_utils import ist_to_utc
from backend.mailer import send_task_created_email, send_completion_email
import os
import psycopg2.extras

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "taskpulse-secret")

# --- Home page / user signup ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        gender = request.form["gender"]

        try:
            conn = get_db_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # Check if user exists
            cur.execute("SELECT id FROM users WHERE email=%s", (email,))
            user = cur.fetchone()

            if user:
                user_id = user["id"]
            else:
                # Insert new user
                cur.execute("""
                    INSERT INTO users (name, email, gender)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """, (name, email, gender))
                user_id = cur.fetchone()["id"]
                conn.commit()

        except Exception as e:
            print("❌ Database error on signup:", e)
            return "Database error. Try again later.", 500
        finally:
            cur.close()
            conn.close()

        return redirect(url_for("tasks", user_id=user_id))

    return render_template("index.html")


# --- Tasks page ---
@app.route("/tasks/<int:user_id>", methods=["GET", "POST"])
def tasks(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

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
                user = cur.fetchone()
                send_task_created_email(user["email"], user["name"], title, due_ist)

                conn.commit()

        # Fetch all tasks
        cur.execute("""
            SELECT id, title, due_time, completed
            FROM tasks
            WHERE user_id=%s
            ORDER BY completed ASC, due_time ASC
        """, (user_id,))
        db_tasks = cur.fetchall()

        tasks_list = []
        for task in db_tasks:
            task_id, title, due_time, completed = task["id"], task["title"], task["due_time"], task["completed"]
            formatted_due = due_time.strftime("%Y-%m-%d %H:%M") if due_time else "No date"
            tasks_list.append((task_id, title, formatted_due, completed))

        incomplete_tasks = [t for t in tasks_list if not t[3]]
        remaining_slots = max(0, 10 - len(incomplete_tasks))

    except Exception as e:
        print("❌ Database error on tasks page:", e)
        return "Database error. Try again later.", 500
    finally:
        cur.close()
        conn.close()

    return render_template("tasks.html",
                           tasks=tasks_list,
                           user_id=user_id,
                           remaining_slots=remaining_slots)


# --- Complete a task ---
@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute("""
            UPDATE tasks
            SET completed = TRUE
            WHERE id=%s
            RETURNING user_id, title
        """, (task_id,))
        task = cur.fetchone()

        if task:
            user_id, title = task["user_id"], task["title"]
            cur.execute("SELECT name, email FROM users WHERE id=%s", (user_id,))
            user = cur.fetchone()
            send_completion_email(user["email"], user["name"], title)
            conn.commit()
            return redirect(url_for("tasks", user_id=user_id))

    except Exception as e:
        print("❌ Database error on complete task:", e)
    finally:
        cur.close()
        conn.close()

    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
