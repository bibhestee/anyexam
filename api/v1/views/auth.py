#!/usr/bin/env python3
"""
Authentication Routes
"""
from flask import Blueprint, request, jsonify
from api import app
from api.models.admin import Admin
from api.models.db import Database
from api.v1.utils.pwdvalidator import hash_password
from api.v1.utils.verify_credentials import verify_credentials
import jwt
from datetime import datetime, timedelta

bp  = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
db = Database()


@bp.route('/signup', methods=['POST'], strict_slashes=False)
def signup():
    """ signup route"""
    body = request.get_json()
    firstname = body.get('firstname')
    lastname = body.get('lastname')
    email = body.get('email')
    org = body.get('organization')
    pos = body.get('position')
    password = body.get('password')
    try:
        pwd = hash_password(password)
        data = db.create_model(Admin, email=email, firstname=firstname, 
    lastname=lastname, organization=org, hashed_password=pwd, position=pos)
        return jsonify({
            'status': 'success',
            'message': 'Account created successfully!',
            'data': data
        })
    except ValueError as e:
        message = e.args[0].split('DETAIL:  ')[1]
        return jsonify({
            'status': 'error',
            'message': message
        }), 400
    except AssertionError as e:
        message = e.args[0]
        return jsonify({
            'status': 'error',
            'message': message
        }), 400
    

@bp.route('/signin', methods=['POST'], strict_slashes=False)
@verify_credentials
def signin(email):
    """ signin route"""
    # Get a token with jwt using email
    token = jwt.encode({'email': email, 'exp': datetime.utcnow() + timedelta(hours=12)}, app.config['SECRET_KEY'])
    # Send the token as authorization in the header 
    response = jsonify({
        'status': 'success',
        'message': 'You have successfully login'
    })
    response.headers.set('Authorization', f'Bearer {token}')
    return response