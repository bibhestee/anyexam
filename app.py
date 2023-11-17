#!/usr/bin/env python3
"""This module contains a flask app"""
from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/', strict_slashes=False)
def home():
    """home page"""
    payload = {"about": "about"}
    return jsonify(payload)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")