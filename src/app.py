from flask import Flask, request, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import os
import uuid
from src.logger import setup_logger

# Initialize logger
logger = setup_logger("tiny-flask-api")

app = Flask(__name__)

# Prometheus counters
REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP Requests", ["method", "endpoint", "http_status"]
)

# --- Health endpoint ---
@app.route("/health")
def health():
    REQUEST_COUNT.labels(method="GET", endpoint="/health", http_status=200).inc()
    return jsonify({"status": "ok"}), 200

# --- Hello endpoint ---
@app.route("/hello", methods=["GET", "POST"])
def hello():
    req_id = str(uuid.uuid4())
    try:
        data = request.get_json(force=True, silent=True) or {}
    except Exception:
        data = {}
    name = data.get("name") if isinstance(data, dict) else None
    if not name:
        name = request.args.get("name", "world")

    # Safe logging without `extra` to avoid KeyError
    logger.info(f"[{req_id}] received request at /hello method={request.method} payload={data}")

    # Example business logic: greet
    message = f"Hello, {name}!"
    logger.info(f"[{req_id}] constructed response: {message}")

    REQUEST_COUNT.labels(method=request.method, endpoint="/hello", http_status=200).inc()
    return jsonify({"request_id": req_id, "message": message})

# --- /metrics endpoint ---
@app.route("/metrics")
def metrics():
    resp = generate_latest()
    return (resp, 200, {"Content-Type": CONTENT_TYPE_LATEST})

# --- Global error handler ---
@app.errorhandler(Exception)
def handle_exception(e):
    req_id = str(uuid.uuid4())
    try:
        method = request.method
        path = request.path
    except Exception:
        method = "N/A"
        path = "N/A"

    logger.error(f"[{req_id}] unhandled exception at {path} method={method} error={e}")
    REQUEST_COUNT.labels(method=method, endpoint=path, http_status=500).inc()
    return jsonify({"error": "internal server error", "request_id": req_id}), 500

# --- Main entry ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    logger.info(f"starting app on port={port} debug={debug}")
    app.run(host="0.0.0.0", port=port, debug=debug)
