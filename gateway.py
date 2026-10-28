import os
import requests
from flask import Flask, render_template, request, Response

app = Flask(__name__)
SERVICES = {"auth": "http://127.0.0.1:5001", "ai": "http://127.0.0.1:5003",
            "history": "http://127.0.0.1:5004"}


def forward(base, path):
    try:
        r = requests.request(request.method, f"{base}{path}", json=request.get_json(silent=True),
                             headers={k: v for k, v in request.headers if k.lower() == "authorization"},
                             timeout=120)
        return Response(r.content, r.status_code, content_type=r.headers.get("Content-Type"))
    except requests.RequestException:
        return Response('{"error":"Service unavailable"}', 503, content_type="application/json")


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/humanize")
def humanize():
    return forward(SERVICES["ai"], "/ai/humanize")


@app.get("/api/health")
def health():
    return forward(SERVICES["ai"], "/health")


@app.route("/api/history", methods=["GET", "POST"])
def history():
    return forward(SERVICES["history"], "/history")


@app.delete("/api/history/<int:record_id>")
def history_delete(record_id):
    return forward(SERVICES["history"], f"/history/{record_id}")


@app.route("/api/auth/<path:p>", methods=["GET", "POST"])
def auth(p):
    return forward(SERVICES["auth"], f"/auth/{p}")


if __name__ == "__main__":
    host = os.getenv("GATEWAY_HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    app.run(host=host, port=port, debug=False)