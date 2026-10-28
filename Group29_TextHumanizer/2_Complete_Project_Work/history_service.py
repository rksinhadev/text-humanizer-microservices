
from flask import Flask, request, jsonify
from functools import wraps
import jwt
import os
from dotenv import load_dotenv
from db import get_connection

load_dotenv()

app = Flask(__name__)

JWT_SECRET = os.getenv("JWT_SECRET")
MAX_TEXT_LENGTH = 20000


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not JWT_SECRET:
            return jsonify({"error": "JWT_SECRET is not configured"}), 500

        auth_header = request.headers.get("Authorization", "")
        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error": "Bearer token required"}), 401

        try:
            payload = jwt.decode(
                parts[1],
                JWT_SECRET,
                algorithms=["HS256"]
            )
            user_id = payload.get("user_id", payload.get("id"))

            if user_id is None:
                return jsonify({"error": "Invalid token payload"}), 401

            request.user_id = int(user_id)

        except (jwt.InvalidTokenError, TypeError, ValueError):
            return jsonify({"error": "Invalid or expired token"}), 401

        return func(*args, **kwargs)

    return wrapper


@app.get("/health")
def health():
    return jsonify({
        "service": "history-service",
        "status": "ok"
    })


@app.post("/history")
@token_required
def create_history():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON body is required"}), 400

    original_text = data.get("original_text")
    humanized_text = data.get("humanized_text")
    tone = data.get("tone", "natural")
    status = data.get("status", "completed")

    if not isinstance(original_text, str) or not original_text.strip():
        return jsonify({"error": "original_text is required"}), 400

    if len(original_text) > MAX_TEXT_LENGTH:
        return jsonify({"error": "Original text is too long"}), 400

    if humanized_text is not None and not isinstance(humanized_text, str):
        return jsonify({"error": "humanized_text must be a string"}), 400

    if humanized_text is not None and len(humanized_text) > MAX_TEXT_LENGTH:
        return jsonify({"error": "Humanized text is too long"}), 400

    if tone not in {"natural", "formal", "casual", "academic"}:
        return jsonify({"error": "Invalid tone"}), 400

    if status not in {"pending", "completed", "failed"}:
        return jsonify({"error": "Invalid status"}), 400

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO text_records
                (user_id, original_text, humanized_text, tone, status)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                request.user_id,
                original_text.strip(),
                humanized_text,
                tone,
                status
            )
        )

        record_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO humanization_logs
                (record_id, service_name, status, message)
            VALUES (%s, %s, %s, %s)
            """,
            (
                record_id,
                "history-service",
                "success",
                "History record created"
            )
        )

        connection.commit()

        return jsonify({
            "message": "History saved successfully",
            "record_id": record_id
        }), 201

    except Exception:
        if connection:
            connection.rollback()

        app.logger.exception("Failed to save history")
        return jsonify({"error": "Could not save history"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


@app.get("/history")
@token_required
def get_history():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, original_text, humanized_text, tone, status, created_at
            FROM text_records
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (request.user_id,)
        )

        records = cursor.fetchall()

        return jsonify({"history": records}), 200

    except Exception:
        app.logger.exception("Failed to retrieve history")
        return jsonify({"error": "Could not retrieve history"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


@app.delete("/history/<int:record_id>")
@token_required
def delete_history(record_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM text_records
            WHERE id = %s AND user_id = %s
            """,
            (record_id, request.user_id)
        )

        if cursor.rowcount == 0:
            connection.rollback()
            return jsonify({
                "error": "History record not found"
            }), 404

        connection.commit()

        return jsonify({
            "message": "History deleted successfully"
        }), 200

    except Exception:
        if connection:
            connection.rollback()

        app.logger.exception("Failed to delete history")
        return jsonify({"error": "Could not delete history"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5004, debug=False)
