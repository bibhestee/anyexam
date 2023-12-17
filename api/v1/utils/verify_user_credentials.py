#!usr/bin/env python3
""" Verify candidate login credentials """
from functools import wraps
from flask import request, jsonify
from api.models import db_engine as db
from api.models.admin import Admin
from api.models.candidate import Candidate
from api.models.exam import Exam

def verify_candidate_credentials(f):
    """ verify candidate login credientials """
    @wraps(f)
    def decorated(*args, **kwargs):
        """ wrapper function """
        # get token from request
        email = request.get_json().get('email')
        token = request.form.get('token')
        if not email:
            payload = {
                'status': 'error',
                'message': 'Email address is required'
            }
            return jsonify(payload), 400
        if not token:
            payload = {
                'status': 'error',
                'message': 'Token is required'
            }
            return jsonify(payload), 400
        # check if candidate's email is already registered
        candidate = db.session.execute(db.select(Candidate).filter_by(email=email)).first()
        if not candidate:
            payload = {
                'status': 'error',
                'message': 'This email is not eligible for this exam'
            }
            return jsonify(payload), 400
        # check if token is correct
        # if token != exam[0].token:
        #     payload = {
        #         'status': 'error',
        #         'message': 'Token is incorrect'
        #     }
        #     return jsonify(payload), 400
        # Return the email address
        return f(email, *args, **kwargs)

    return decorated