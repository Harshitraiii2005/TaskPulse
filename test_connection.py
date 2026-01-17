import psycopg2


conn_string = "postgresql://neondb_owner:npg_rXlF3Y6ZHwof@ep-crimson-king-a1d904w4-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

try:
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    result = cur.fetchone()
    print("✅ Connection successful! Current time:", result)
    cur.close()
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)
