#!/usr/bin/env python3
"""
Quiz Routes
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.models.db import Database
from api.v1.utils.files_handler import upload, get_all_files, load_file
from api.v1.utils.token_required import token_required
from api.v1.utils.verify_user_credentials import verify_candidate_credentials
from api.models.exam import Exam
from api.models.result import Result
import os
from random import shuffle, random
from math import floor

bp  = Blueprint('quiz', __name__, url_prefix='/api/v1/quiz')
db = Database()


@bp.route('/start', methods=['POST'], strict_slashes=False)
@verify_candidate_credentials
def start_exam(exam):
    """ POST /api/v1/quiz/start
    """
    no_of_questions = exam.get('no_of_questions')
    exam_id = exam.get('exam_id')
    duration = exam.get('duration')
    # Get the folder name
    from api import app
    folder = os.path.join(app.config['UPLOAD_FOLDER'], exam_id)
    # load the question
    files = get_all_files(folder)
    questions = []
    for file in files:
        filename = os.path.join(folder, file)
        try:
            contents = load_file(filename)
        except AttributeError as e:
            return jsonify({
                'status': 'error',
                'message': f'Internal server error: {e}'
            }), 500
        if contents:
            questions.extend(contents)
    if len(questions) < no_of_questions:
        return jsonify({
            'status': 'error',
            'message': 'The number of available question is less than the question set for this exam'
        })
    # shuffle the question
    times = floor(random() * 10)
    for i in range(times + 1 ):
        shuffle(questions)
    # return the question
    return jsonify({
        'status': 'success',
        'message': 'You can start you exam now',
        'data': {
            'title': exam.get('title'),
            'type': exam.get('exam_type'),
            'questions': questions[:no_of_questions],
            'duration': duration
        }
    })


@bp.route('/upload/<exam_id>', methods=['POST'], strict_slashes=False)
@token_required
def upload_question(current_user, exam_id):
    """ POST /api/v1/quiz/upload/<exam_id>
    """
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


@bp.route('/questionbank/<exam_id>', methods=['GET'], strict_slashes=False)
@token_required
def load_question_bank(current_user, exam_id):
    """ GET /api/v1/quiz/questionbank/<exam_id>
    """
    # Check if folder exists
    from api import app
    folder = os.path.join(app.config['UPLOAD_FOLDER'], exam_id)
    if not os.path.exists(folder):
        return jsonify({
            'status': 'error',
            'message': 'Folder not found: invalid exam id'
        }), 400
    # Get all the files in the directory
    files = get_all_files(folder)
    return jsonify({
        'status': 'success',
        'message': 'Question bank files retrieved successfully',
        'data': files
    })


@bp.route('/questionbank/<exam_id>/', methods=['DELETE'], strict_slashes=False)
@token_required
def delete_question_bank(current_user, exam_id):
    """ GET /api/v1/quiz/questionbank/<exam_id>
    """
    # Check if folder exists
    from api import app
    folder = os.path.join(app.config['UPLOAD_FOLDER'], exam_id)
    if not os.path.exists(folder):
        return jsonify({
            'status': 'error',
            'message': 'Folder not found: invalid exam id'
        }), 400
    import shutil
    shutil.rmtree(folder)
    return jsonify({
        'status': 'success',
        'message': 'All question bank deleted'
    })


@bp.route('/submit', methods=['POST'], strict_slashes=False)
def submit_exam():
    """ submit exam """
    body: dict = request.get_json()
    token: str = body.get('token')
    score: int = body.get('score')
    if not token:
        return jsonify({
            'status': 'error',
            'message': 'Token is required'
        }), 400
    if not score:
        return jsonify({
            'status': 'error',
            'message': 'Score is required'
        }), 400
    if type(score) != int:
        return jsonify({
            'status': 'error',
            'message': 'Score should be of type Integer'
        }), 400
    # check if token is correct
    try:
        option: dict = {'token': token}
        result: Result = db.get_by(Result, **option)
        candidate: Result = result.to_json()
        # check if token is used
        if candidate.get('token_used'):
            return jsonify({
                'status': 'error',
                'message': 'Unable to submit exam, exam token already used'
            }), 400
        if not candidate.get('email'):
            return jsonify({
                'status': 'error',
                'message': 'Start the exam before submitting a score'
            }), 400
    except (NoResultFound, MultipleResultsFound):
        return jsonify({
            'status': 'error',
            'message': 'Incorrect token supplied'
        }), 400
    data: dict = {
        'token_used': True,
        'score': score if score > 0 and score < 50 else 0
    }
    try:
        id = candidate.get('result_id')
        db.update(Result, id, **data)
        return jsonify({
            'status': 'success',
            'message': 'Exam submitted successfully'
        })
    except (ValueError, AttributeError):
        return jsonify({
            'status': 'error',
            'message': 'Unable to update exam condition'
        }), 500