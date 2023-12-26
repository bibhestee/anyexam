#!/usr/bin/env python3
"""
Exam Routes
"""
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.exc import DataError
from api.models.admin import Admin
from api.models.exam import Exam
from api.models.result import Result
from api.models.db import Database
from api.v1.utils.token_required import token_required
from api.v1.utils.misc import generate_candidate_token



bp = Blueprint('exam', __name__, url_prefix='/api/v1/admins/exams')
db = Database()



@bp.route('/', methods=['POST'], strict_slashes=False)
@token_required
def exam_condition(current_user):
    """ POST /api/v1/admins/exams
    Form data
        title: title of the exam.
        exam_type: type of the exam.
        duration: duration of the exam.
        no_of_questions: Number of question for the exam.
        result: Handle result's visibility to candidate.
        admin_id: Admin id
    """
    title = request.get_json().get('title')
    exam_type = request.get_json().get('exam_type')
    duration = request.get_json().get('duration')
    no_of_questions = request.get_json().get('no_of_questions')
    result = request.get_json().get('result')
    try:
        data = db.create_model(Exam, title=title, exam_type=exam_type, duration=duration, no_of_questions=no_of_questions, result=result, admin_id=current_user.id)
        return jsonify({
            'status': 'success',
            'message': 'Exam conditions set successfully!',
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
    except Exception as e:
        print(e)
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500


@bp.route('/', methods=['GET'], strict_slashes=False)
def get_all_exam():
    """ GET /api/v1/admins/exams
    Return:
      - list of all Exam objects JSON represented
    """
    exams = db.get_all(Exam)
    return jsonify(exams)


@bp.route('/<exam_id>', methods=['GET'], strict_slashes=False)
@token_required
def get_exam(exam_id: str):
    """ GET /api/v1/admins/exams
    Return:
      - Exam object JSON represented
    """
    if not exam_id:
        abort(404)
    try:
        exam = db.get_model(Exam, exam_id)
        if not exam:
            abort(404)
    except DataError:
        abort(404)
    return jsonify({
            'status': 'success',
            'data': exam.to_json(),
            'message': 'exam retrieved successfully'
        })


@bp.route('/<exam_id>', methods=['PUT'], strict_slashes=False)
@token_required
def update_exam(current_user, exam_id: str):
    """ PUT /api/v1/admins/exams/<exam_id>
    Path parameter:
        - exam_id
    Return:
        - update the Exam objects
    """
    if not exam_id:
        abort(404)
    data = request.get_json()
    if not data:
        payload = {
            'status': 'error',
            'message': 'Wrong format: check the request data'
        }
        return jsonify(payload), 400
    try:
        updatedModel = db.update(Exam, exam_id, **data)
        return jsonify({'data': updatedModel.to_json()}), 200
    except ValueError:
        abort(404)
    except AttributeError:
        return jsonify({
            'status': 'error',
            'message': 'Invalid update field'
        }), 400
    except DataError:
        abort(404)


@bp.route('/generate_token/<exam_id>', methods=['GET'], strict_slashes=False)
@token_required
def generate_exam_token(current_user, exam_id: str):
    """ PUT /api/v1/admins/exams/generate_token/<exam_id>
    Path parameter:
        - exam_id
    Return:
        - generated token
    """
    if not exam_id:
        return jsonify({
            'status': 'error',
            'message': 'Exam id is required: add id to the endpoint'
        }), 400
    exam = db.get_model(Exam, exam_id)
    # Generate exam token
    token = generate_candidate_token()
    # Create a result model and return the token
    try:
        data = db.create_model(Result, token=token, exam_id=exam.id, admin_id=current_user.id)
        return jsonify({
            'status': 'success',
            'token': token,
            'message': 'Token generated successfully'
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
    except Exception as e:
        print(e)
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500


@bp.route('/results', methods=['GET'], strict_slashes=False)
def get_result():
    """ GET /api/v1/admins/exams/results
    Return:
        - all the result objects
    """
    results = db.get_all(Result)
    return jsonify(results)


@bp.route('/<exam_id>/results', methods=['GET'], strict_slashes=False)
def get_result_by_exam(exam_id):
    """ GET /api/v1/admins/exams/<exam_id>/results
    Path parameter:
        - exam_id
    Return:
        - Results of all exam with the id
    """
    exam = db.get_model(Exam, exam_id)
    results = db.get_exam_results(Result, exam_id)
    return jsonify({
        'status': 'success',
        'message': 'Results retrieved successfully',
        'data': {
            'exam': exam,
            'results': results
        }
    })


@bp.route('/results/<result_id>', methods=['GET'], strict_slashes=False)
def get_result(result_id: str):
    """ GET /api/v1/admins/exams/results/<result_id>
    Path parameter:
        - result_id
    Return:
        - a single result with the id
    """
    result = db.get_model(Result, result_id)
    return jsonify({
        'status': 'success',
        'message': 'Result retrieved successfully',
        'data': result
    })
