#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import auth
from flask import Flask, jsonify
from flask_cors import (CORS, cross_origin)
from api.v1.utils.config import Config
from models.db import Database


app = Flask(__name__)
app.config.from_object(Config)
# Blueprint registrations
app.register_blueprint(auth.bp)
# Connect the app to database 
Database().db.init_app(app)
# Allow cross origin on incoming requests
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.route('/')
@app.route('/api')
@app.route('/api/v1')
def home():
    return 'You just hit the anyexam api base url - add resource to the baseURL to access resources'


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    payload = {
        'status': 'error',
        'message': 'Not found'
    }
    return jsonify(payload), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    payload = {
        'status': 'error',
        'message': 'Unauthorized'
    }
    return jsonify(payload), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden error handler
    """
    payload = {
        'status': 'error',
        'message': 'Forbidden'
    }
    return jsonify(payload), 403