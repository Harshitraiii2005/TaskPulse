import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    DATABASE_URL = os.getenv(DATABASE_URL)
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set!")

    try:
        
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except psycopg2.OperationalError as e:
        print("Failed to connect to the database!")
        print("Check your DATABASE_URL and network access to Neon DB.")
        print("Error details:", e)
        raise  
