from flask import Flask, request, jsonify

app = Flask(__name__)

MAX_TEXT_LENGTH = 20000

ALLOWED_TONES = {
    "natural",
    "formal",
    "casual",
    "academic"
}


def mock_humanize(text, tone):
    """
    Temporary mock implementation.
    Replace this function with a real AI provider later.
    It does NOT actually rewrite the text.
    """
    return f"[MOCK - {tone.upper()}] {text}"


@app.get("/health")
def health():
    return jsonify({
        "service": "ai-service",
        "status": "ok",
        "mode": "mock"
    }), 200


@app.post("/ai/humanize")
def humanize():
    data = request.get_json(silent=True) or {}

    text = data.get("text")
    tone = data.get("tone", "natural")

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

    if not isinstance(tone, str) or tone not in ALLOWED_TONES:
        return jsonify({
            "error": "Invalid tone",
            "allowed_tones": sorted(ALLOWED_TONES)
        }), 400

    humanized_text = mock_humanize(text, tone)

    return jsonify({
        "message": "Mock response generated",
        "mode": "mock",
        "tone": tone,
        "original_text": text,
        "humanized_text": humanized_text
    }), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5003, debug=False)