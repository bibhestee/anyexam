from flask import Blueprint, jsonify

main = Blueprint('main', __name__)


@main.route('/', strict_slashes=False)
def home():
    """home page"""
    payload = {"about": "about"}
    return jsonify(payload)