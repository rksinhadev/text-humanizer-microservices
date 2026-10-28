
import os
from datetime import datetime, timedelta, timezone
from functools import wraps

import bcrypt
import jwt
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, request, jsonify, g

load_dotenv()

app = Flask(__name__)

PORT = 5001
JWT_SECRET = os.getenv("JWT_SECRET")

if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET .env file mein set karo")


def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "text_humanizer")
    )


def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=2)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error": "Bearer token required"}), 401

        try:
            payload = jwt.decode(
                parts[1], JWT_SECRET, algorithms=["HS256"]
            )
            g.user_id = int(payload["user_id"])
        except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
            return jsonify({"error": "Invalid or expired token"}), 401

        return func(*args, **kwargs)

    return wrapper


@app.post("/auth/signup")
def signup():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({
            "error": "Name, email and password are required"
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": "Password must be at least 8 characters"
        }), 400

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) "
            "VALUES (%s, %s, %s)",
            (name, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid

        return jsonify({
            "message": "Signup successful",
            "user": {"id": user_id, "name": name, "email": email}
        }), 201

    except mysql.connector.IntegrityError:
        return jsonify({"error": "Email already registered"}), 409
    except mysql.connector.Error:
        app.logger.exception("Database error during signup")
        return jsonify({"error": "Database operation failed"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.post("/auth/login")
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, name, email, password_hash "
            "FROM users WHERE email = %s",
            (email,)
        )
        user = cursor.fetchone()

        if not user or not bcrypt.checkpw(
            password.encode("utf-8"),
            user["password_hash"].encode("utf-8")
        ):
            return jsonify({"error": "Invalid email or password"}), 401

        token = create_token(user["id"])

        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }
        }), 200

    except mysql.connector.Error:
        app.logger.exception("Database error during login")
        return jsonify({"error": "Database operation failed"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.get("/auth/me")
@token_required
def get_current_user():
    conn = None
    cursor = None

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, name, email FROM users WHERE id = %s",
            (g.user_id,)
        )
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"user": user}), 200
    except mysql.connector.Error:
        app.logger.exception("Database error while reading user")
        return jsonify({"error": "Database operation failed"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.get("/health")
def health():
    return jsonify({"service": "auth-service", "status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=PORT, debug=False)
