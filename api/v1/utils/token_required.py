#!/usr/bin/env python3
""" Token required decorator module """
from flask import request, jsonify
from functools import wraps
import jwt
from api.models.db import Database as db
from api.models.admin import Admin
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth = None
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
            from api import app
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            email = data.get('email')
            from api.models import db_engine
            current_user = db_engine.session.execute(db_engine.select(Admin).filter_by(email=email)).unique().scalar_one()
        except jwt.ExpiredSignatureError:
            return jsonify({
                'status': 'error',
                'message': 'You token has expired, login to generate new token'
            }), 401
        except (jwt.InvalidTokenError, NoResultFound, MultipleResultsFound):
            payload = {
                'status': 'error',
                'message' : 'Token supplied is invalid'
            }
            return jsonify(payload), 401
        
        # returns the current logged in users context to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated