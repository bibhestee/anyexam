#!/usr/bin/env python3
""" Token required decorator module """
from flask import request, jsonify
from functools import wraps
import jwt
from api import app
from api.models.db import Database as db
from api.models.admin import Admin


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Get token from request header
        if 'Authorization' in request.headers:
            auth = request.headers['Authorization']
        # return 401 if token is not passed
        if not auth:
            payload = {
                'status': 'error',
                'message': 'No token supplied'
            }
            return jsonify(payload), 401
  
        try:
            # Extract token from bearer token jwt
            token = auth.split(' ')[1]
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = db().get_model(Admin, email=data.email)
        except jwt.ExpiredSignatureError:
            return jsonify({
                'status': 'error',
                'message': 'You token has expired, login to generate new token'
            }), 401
        except jwt.InvalidTokenError:
            payload = {
                'status': 'error',
                'message' : 'Token supplied is invalid'
            }
            return jsonify(payload), 401
        
        # returns the current logged in users context to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated