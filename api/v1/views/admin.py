#!/usr/bin/env python3
"""
Admin Routes
"""
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.exc import DataError
from api.models.admin import Admin
from api.models.exam import Exam
from api.models.db import Database
from api.v1.utils.token_required import token_required


bp = Blueprint('admin', __name__, url_prefix='/api/v1/admins')
db = Database()


@bp.route('/<admin_id>', methods=['GET'], strict_slashes=False)
def get_one_admin(admin_id: str = None) -> str:
    """ GET /api/v1/admins/:admin_id
        Path parameter:
        - Admin ID
        Return:
        - Admin object JSON represented
        - 404 if the Admin ID doesn't exist
    """
    if not admin_id:
        abort(404)
    try:
        admin = db.get_model(Admin, admin_id)
        if not admin:
            abort(404)
    except DataError:
        abort(404)
    return jsonify({
            'status': 'success',
            'data': admin.to_json(),
            'message': 'Admin retrieved successfully'
        })


@bp.route('/', methods=['GET'], strict_slashes=False)
def view_all_admins() -> str:
    """ GET /api/v1/admins
    Return:
      - list of all Admin objects JSON represented
    """
    all_admins = db.get_all(Admin)
    return jsonify(all_admins)


@bp.route('/<admin_id>', methods=['PUT'], strict_slashes=False)
@token_required
def update_admin(current_user, admin_id: str = None) -> str:
    """ PUT /api/v1/admins/:id
    Path parameter:
      - admin ID
    JSON body:
      - last_name (optional)
      - first_name (optional)
      - organization (optional)
      - position (optional)
    Return:
      - admin object JSON represented
      - 404 if the admin ID doesn't exist
      - 400 if can't update the admin
    """
    if not admin_id:
        abort(404)
    data = request.get_json()
    if not data:
        payload = {
            'status': 'error',
            'message': 'Wrong format: check the request data'
        }
        return jsonify(payload), 400
    try:
        updatedModel = db.update(Admin, admin_id, **data)
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


@bp.route('/<admin_id>', methods=['DELETE'], strict_slashes=False)
def delete_admin(admin_id: str = None) -> str:
    """ DELETE /api/v1/admins/:id
    Path parameter:
      - admin ID
    Return:
      - empty JSON is the admin has been correctly deleted
      - 404 if the admin ID doesn't exist
    """
    if not admin_id:
        abort(404)
    try:
        admin = db.get_model(Admin, admin_id)
        if not admin:
            abort(404)
    except DataError:
        abort(404)
    db.delete(admin)
    return jsonify({}), 203


@bp.route('/exams', methods=['POST'], strict_slashes=False)
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


@bp.route('/exams', methods=['GET'], strict_slashes=False)
def get_all_exam():
    """ GET /api/v1/admins/exams
    Return:
      - list of all Exam objects JSON represented
    """
    exams = db.get_all(Exam)
    return jsonify(exams)


@bp.route('/exams/<exam_id>', methods=['GET'], strict_slashes=False)
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


@bp.route('/myexams/<admin_id>', methods=['GET'], strict_slashes=False)
def get_all_my_exams(admin_id: str):
    """ GET /api/v1/admins/myexams
    Return:
      - list of all Exam objects JSON represented by admin
    """
    exams = db.get_my_exams(Exam, admin_id)
    return jsonify(exams)


@bp.route('/exams/<exam_id>', methods=['PUT'], strict_slashes=False)
@token_required
def update_exam(current_user, exam_id: str):
    """ PUT /api/v1/admins/exams
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
