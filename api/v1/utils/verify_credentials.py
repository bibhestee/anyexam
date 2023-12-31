#!/usr/bin/env python3
""" Verify login credentials """
from functools import wraps
from flask import request, jsonify
from werkzeug.security import check_password_hash
from api.models import db_engine as db
from api.models.admin import Admin


def verify_credentials(f):
    """ verify login credentials """
    @wraps(f)
    def decorated(*args, **kwargs):
        """ function wrapper """
        # get password and email from request
        email = request.get_json().get('email')
        password = request.get_json().get('password')
        if not email:
            payload = {
                'status': 'error',
                'message': 'Email address is required'
            }
            return jsonify(payload), 400
        if not password:
            payload = {
                'status': 'error',
                'message': 'Password is required'
            }
            return jsonify(payload), 400
        # Check if the email is already registered
        admin = db.session.execute(db.select(Admin).filter_by(email=email)).first()
        if not admin:
            payload = {
               'status': 'error',
              'message': 'Email address is not registered'
            }
            return jsonify(payload), 400
        # Check if the password is correct
        if not check_password_hash(admin[0].hashed_password, password):
            payload = {
               'status': 'error',
              'message': 'Password is incorrect'
            }
            return jsonify(payload), 400
        # Return the email address
        return f(email, *args, **kwargs)

    return decorated