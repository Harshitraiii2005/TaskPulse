import psycopg2

conn_string = "postgresql://neondb_owner:npg_rXlF3Y6ZHwof@ep-crimson-king-a1d904w4-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

conn = psycopg2.connect(conn_string)
cur = conn.cursor()

# Users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    gender TEXT
);
""")

# Tasks table
cur.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    title TEXT NOT NULL,
    due_time TIMESTAMP NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    last_notified TIMESTAMP
    
);
""")




conn.commit()
cur.close()
conn.close()

print("✅ Tables created successfully!")
