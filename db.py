import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "Sahil@1844"),
        database=os.getenv("DB_NAME", "text_humanizer"),
    )


if __name__ == "__main__":
    try:
        connection = get_connection()
        print("MySQL connected successfully!")

        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE()")
        print("Database:", cursor.fetchone()[0])
        cursor.execute("SHOW TABLES")
        print("Tables:", [row[0] for row in cursor.fetchall()])

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        print("Database connection failed:", error)