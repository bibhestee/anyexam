#!/usr/bin/env python3
"""
Authentication Routes
"""
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from api.models.admin import Admin
from api.models.db import Database

bp  = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
db = Database()


@bp.route('/signup', methods=['POST'], strict_slashes=False)
def admin_signup():
    """admin signup route"""
    body = request.form.to_dict()
    firstname = body.get('firstname')
    lastname = body.get('lastname')
    email = body.get('email')
    org = body.get('organization')
    pos = body.get('position')
    password = body.get('password')
    if not firstname:
        return jsonify({
            'status': 'error',
            'message': 'first name is missing'
        }), 400
    if not lastname:
        return jsonify({
            'status': 'error',
            'message': 'last name is missing'
        }), 400
    if not email:
        return jsonify({
            'status': 'error',
            'message': 'email is missing'
        }), 400
    if not org:
        return jsonify({
            'status': 'error',
            'message': 'organization is missing'
        }), 400
    if not pos:
        return jsonify({
            'status': 'error',
            'message': 'position is missing'
        }), 400
    if not password:
        return jsonify({
            'status': 'error',
            'message': 'password is missing'
        }), 400

    pwd = generate_password_hash(password)
    data = db.create_model(Admin, email=email, firstname=firstname, 
    lastname=lastname, organization=org, hashed_password=pwd, position=pos)
    if data.get('error'):
        return jsonify({
            'status': 'error',
            'message': data.get('error')
        }), 400
    return jsonify({
        'status': 'success',
        'message': 'Account created successfully!',
        'data': data.to_json()
    })
