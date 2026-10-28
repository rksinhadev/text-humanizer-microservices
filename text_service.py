import re
from flask import Flask, request, jsonify

app = Flask(__name__)

MAX_TEXT_LENGTH = 20000


def count_words(text):
    return len(re.findall(r"\b[\w'-]+\b", text))


@app.get("/health")
def health():
    return jsonify({
        "service": "text-service",
        "status": "ok"
    }), 200


@app.post("/text/validate")
def validate_text():
    data = request.get_json(silent=True) or {}

    text = data.get("text")

    if not isinstance(text, str):
        return jsonify({
            "error": "Text must be a string"
        }), 400

    text = text.strip()

    if not text:
        return jsonify({
            "error": "Text cannot be empty"
        }), 400

    if len(text) > MAX_TEXT_LENGTH:
        return jsonify({
            "error": f"Text cannot exceed {MAX_TEXT_LENGTH} characters"
        }), 400

    return jsonify({
        "message": "Text validated successfully",
        "text": text,
        "word_count": count_words(text),
        "character_count": len(text)
    }), 200


@app.post("/text/prepare")
def prepare_text():
    data = request.get_json(silent=True) or {}

    text = data.get("text")
    tone = data.get("tone", "natural")

    allowed_tones = [
        "natural",
        "formal",
        "casual",
        "academic"
    ]

    if not isinstance(text, str):
        return jsonify({"error": "Text must be a string"}), 400

    text = text.strip()

    if not text:
        return jsonify({"error": "Text cannot be empty"}), 400

    if len(text) > MAX_TEXT_LENGTH:
        return jsonify({
            "error": f"Text cannot exceed {MAX_TEXT_LENGTH} characters"
        }), 400

    if not isinstance(tone, str) or tone not in allowed_tones:
        return jsonify({
            "error": "Invalid tone",
            "allowed_tones": allowed_tones
        }), 400

    return jsonify({
        "message": "Text prepared successfully",
        "text": text,
        "tone": tone,
        "word_count": count_words(text),
        "character_count": len(text)
    }), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=False)