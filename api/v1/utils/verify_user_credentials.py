#!usr/bin/env python3
""" Verify candidate login credentials """
from functools import wraps
from flask import request, jsonify
from api.models import db_engine as db
from api.models.result import Result
from api.models.exam import Exam


def verify_candidate_credentials(f):
    """ verify candidate login credientials """
    @wraps(f)
    def decorated(*args, **kwargs):
        """ wrapper function """
        # get token from request
        email = request.get_json().get('email')
        token = request.get_json().get('token')
        firstname = request.get_json().get('firstname')
        lastname = request.get_json().get('lastname')
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
        if not firstname:
            payload = {
                'status': 'error',
                'message': 'Firstname is required'
            }
            return jsonify(payload), 400
        elif len(firstname) < 3 or len(firstname) > 25:
            payload = {
                'status': 'error',
                'message': 'Firstname should be min of 3 and max of 25 characters'
            }
            return jsonify(payload), 400

        if not lastname:
            payload = {
                'status': 'error',
                'message': 'Lastname is required'
            }
            return jsonify(payload), 400
        elif len(lastname) < 3 or len(lastname) > 25:
            payload = {
                'status': 'error',
                'message': 'Lastname should be min of 3 and max of 25 characters'
            }
            return jsonify(payload), 400
        
        # check if candidate's email is already registered
        candidate = db.session.execute(db.select(Result).filter_by(email=email)).first()
        if candidate:
            payload = {
                'status': 'error',
                'message': 'Email is already used by another candidate'
            }
            return jsonify(payload), 400
        # check if token is correct
        if token != candidate.get('token'):
            payload = {
                'status': 'error',
                'message': 'Incorrect token supplied'
            }
            return jsonify(payload), 400
        # check if token is used
        if candidate.get('token_used'):
            payload = {
                'status': 'error',
                'message': 'Exam token already used. Generate a new token'
            }
            return jsonify(payload), 400
        data = {
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
        }
        # Use the exam id to get the exam condition
        from api.models.db import Database as d
        exam_id = candidate.get('exam_id')
        id = candidate.get('id')
        exam = d.get_model(Exam, exam_id)
        try:
            d.update(Result, id, **data)
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': 'Unable to update exam condition'
            }), 500
        # Return exam condition
        return f(exam.to_json(), *args, **kwargs)

    return decorated