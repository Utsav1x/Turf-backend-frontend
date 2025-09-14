from fastapi import HTTPException
import mysql.connector
import os
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()


DB_CONFIG = {
    'host': os.getenv("MYSQL_HOST","localhost"),
    'user': os.getenv("MYSQL_USER"),
    'password': os.getenv("MYSQL_PASSWORD"),
    'database': os.getenv("MYSQL_DATABASE"),
    'port': int(os.getenv("MYSQL_PORT",3306))
}

@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        yield conn
    except mysql.connector.Error as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if conn and conn.is_connected():
            conn.close()


def execute_query(query:str, params: tuple = None, fetch: str = None):
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())

            if fetch == "one":
                return cursor.fetchone()
            elif fetch =="all":
                return cursor.fetchall()
            else:
                conn.commit()
                return cursor.lastrowid if cursor.lastrowid else cursor.rowcount
        finally:
            cursor.close()
