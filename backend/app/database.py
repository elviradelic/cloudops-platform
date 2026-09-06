import psycopg2

from app.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=3,
    )


def check_database_connection():
    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            cursor.fetchone()

        connection.close()

        return {
            "status": "connected"
        }

    except Exception as exc:
        return {
            "status": "unavailable",
            "error": str(exc)
        }