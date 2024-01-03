#!/usr/bin/env python3
"""
Authentication Routes
"""
from flask import Blueprint, request, jsonify
from api.models.admin import Admin
from api.models.db import Database
from api.models.candidate import Candidate
from api.v1.utils.pwdvalidator import hash_password
from api.v1.utils.verify_credentials import verify_credentials
from api.v1.utils.verify_user_credentials import verify_candidate_credentials
from api.v1.utils.token_required import token_required
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
    answer = body.get('answer')
    try:
        pwd = hash_password(password)
        data = db.create_model(Admin, email=email, firstname=firstname,
    lastname=lastname, organization=org, hashed_password=pwd, position=pos, answer=answer)
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
def signin(email: str):
    """ signin route"""
    # Get a token with jwt using email
    from api import app
    token = jwt.encode({'email': email, 'exp': datetime.utcnow() + timedelta(hours=12)}, app.config['SECRET_KEY'])
    # Send the token as authorization in the header
    response = jsonify({
        'status': 'success',
        'message': 'You have successfully login'
    })
    response.headers.set('Authorization', f'Bearer {token}')
    return response


@bp.route('/reset-password/<id>', methods=['PUT'], strict_slashes=False)
def reset_password(id: str):
    """ reset password """
    # Get the new password and security answer from the request body
    body = request.get_json()
    new_pwd = body.get('new_password')
    answer = body.get('answer')
    if not new_pwd or not answer:
        return jsonify({
            'status': 'error',
            'message': 'No new password or security question answer supplied'
        }), 400
    admin = db.get_model(Admin, id)
    # Check if security answer matches the answer at registration and
    # Update password if answer matches
    if admin.answer and admin.answer.lower() == answer.lower():
        obj = {
            'hashed_password': hash_password(new_pwd)
        }
        db.update(Admin, id, **obj)
        return jsonify({
            'status': 'success',
            'message': 'password reset was successful'
        }), 200

    return jsonify({
        'status': 'error',
        'message': 'The answer is incorrect, retry. What is your favourite city?'
    }), 400


@bp.route('/user-login', methods=['POST'], strict_slashes=False)
@verify_candidate_credentials
def user_login(email: str, exam_id: str):
    """ Candidate login """
    from api import app
    token = jwt.encode({'email': email, 'exam_id': exam_id, 'exp': datetime.utcnow() + timedelta(hours=2)}, app.config['SECRET_KEY'])
    response = jsonify({
        'status': 'success',
        'message': 'You have successfully logged in'
    })
    response.headers.set('Authorization', f'Bearer {token}')
    return response