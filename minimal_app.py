#!/usr/bin/env python3
"""
Minimal Flask app for Railway deployment
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return jsonify({
        "message": "Hello from Railway!",
        "status": "success",
        "port": os.environ.get('PORT', '8000')
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/test')
def test():
    return jsonify({
        "message": "Test endpoint working",
        "method": request.method
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting minimal app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
