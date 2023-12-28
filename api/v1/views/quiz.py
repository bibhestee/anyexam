#!/usr/bin/env python3
"""
Quiz Routes
"""
from flask import Blueprint, request, jsonify, abort
# from api.models.admin import Admin
from api.models.db import Database
from api.v1.utils.files_handler import upload
from api.v1.utils.token_required import token_required
from api.models.exam import Exam
# from api.v1.utils.pwdvalidator import hash_password
# from api.v1.utils.verify_credentials import verify_credentials
# from api.v1.utils.verify_user_credentials import verify_candidate_credentials
# import jwt
# from datetime import datetime, timedelta

bp  = Blueprint('quiz', __name__, url_prefix='/api/v1/quiz')
db = Database()


@bp.route('/start', methods=['POST'], strict_slashes=False)
def start_exam():
    """ POST /api/v1/quiz/start
    """
    # decode the auth token and get the exam id
    # Get the exam condition
    # load the question
    # shuffle the question
    # return the question in pages


@bp.route('/upload/<exam_id>', methods=['POST'], strict_slashes=False)
@token_required
def upload_question(current_user, exam_id):
    """ POST /api/v1/quiz/upload/<exam_id>
    """
    if not exam_id:
        return jsonify({
            'status': 'error',
            'message': 'No exam provided. Provide the exam id'
        })
    try:
        db.get_model(Exam, exam_id)
        # Get the file(s) from the request method
        files_dict = request.files.to_dict()
        files = list(files_dict.values())
        if len(files) < 1:
            return jsonify({
                'status': 'error',
                'message': 'No file found. Select a file to be uploaded'
            }), 404
        # Create a folder with the exam id
        import os
        from api import app
        folder = os.path.join(app.config['UPLOAD_FOLDER'], exam_id)
        if not os.path.exists(folder):
            os.makedirs(folder)
        # handle the file(s) and upload
        payload = upload(files, folder, current_user)
        if payload['status'] == 'success':
            return jsonify(payload)
        return jsonify(payload), 400
    except Exception:
        return jsonify({
            'status': 'error',
            'message': 'Invalid exam id'
        })
