from flask import Flask, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "payment-api",
        "version": "2.2.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

@app.route("/")
def root():
    return jsonify({
        "service": "payment-api",
        "docs": "/health",
        "openapi": "/openapi/baseline.json"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)