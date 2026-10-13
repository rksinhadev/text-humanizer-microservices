
from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

AUTH_SERVICE = os.getenv("AUTH_SERVICE_URL", "http://127.0.0.1:5001")
TEXT_SERVICE = os.getenv("TEXT_SERVICE_URL", "http://127.0.0.1:5002")
AI_SERVICE = os.getenv("AI_SERVICE_URL", "http://127.0.0.1:5003")
HISTORY_SERVICE = os.getenv("HISTORY_SERVICE_URL", "http://127.0.0.1:5004")

TIMEOUT = 30


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({
        "service": "api-gateway",
        "status": "ok"
    })


def forward_request(base_url, path, method=None):
    method = method or request.method

    try:
        response = requests.request(
            method=method,
            url=f"{base_url}{path}",
            json=request.get_json(silent=True) if method in {"POST", "PUT", "PATCH"} else None,
            params=request.args,
            headers={
                "Authorization": request.headers.get("Authorization", "")
            },
            timeout=TIMEOUT
        )

        try:
            body = response.json()
            return jsonify(body), response.status_code
        except ValueError:
            return response.text, response.status_code

    except requests.RequestException:
        return jsonify({
            "error": "Service unavailable",
            "message": "Please try again later"
        }), 503


# Authentication routes
@app.route("/auth/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def auth_routes(path):
    return forward_request(AUTH_SERVICE, f"/auth/{path}")


# Text processing routes
@app.route("/text/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def text_routes(path):
    return forward_request(TEXT_SERVICE, f"/text/{path}")


# AI routes
@app.route("/ai/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def ai_routes(path):
    return forward_request(AI_SERVICE, f"/ai/{path}")


# History routes
@app.route("/history", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/history/<path:path>", methods=["GET", "POST", "DELETE"])
def history_routes(path):
    suffix = f"/{path}" if path else ""
    return forward_request(HISTORY_SERVICE, f"/history{suffix}")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
