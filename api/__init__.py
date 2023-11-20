#!/usr/bin/env python3
"""
Main API Module
"""
from os import getenv
from api.v1.views import auth
from api.v1.views import admin
from flask import Flask, jsonify
from flask_cors import (CORS, cross_origin)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import MethodNotAllowed
from api.v1.utils.config import Config
from api.models import db_engine

db = db_engine

app = Flask(__name__)
app.config.from_object(Config)
# Blueprint registrations
app.register_blueprint(auth.bp)
app.register_blueprint(admin.bp)
# Connect the app to database 
db.init_app(app)
migrate = Migrate(app, db)
# Import the models
from api.models.admin import Admin
# Create the tables
with app.app_context():
    db.create_all()
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


@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(error) -> str:
    """ Handle not allowed method requests """
    allowed_methods = ', '.join(error.valid_methods)
    payload = {
        'status': 'error',
        'message': 'Unknown endpoint'
    }
    return jsonify(payload), 405