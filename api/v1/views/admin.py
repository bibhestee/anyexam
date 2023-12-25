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


@bp.route('/', methods=['PUT'], strict_slashes=False)
@token_required
def update_admin(current_user) -> str:
    """ PUT /api/v1/admins/
    JSON body:
      - last_name (optional)
      - first_name (optional)
      - organization (optional)
      - position (optional)
    Return:
      - admin object JSON represented
      - 400 if can't update the admin
    """
    data = request.get_json()
    if not data:
        payload = {
            'status': 'error',
            'message': 'Wrong format: check the request data'
        }
        return jsonify(payload), 400
    try:
        updatedModel = db.update(Admin, current_user.id, **data)
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


@bp.route('/myexams', methods=['GET'], strict_slashes=False)
@token_required
def get_all_my_exams(current_user):
    """ GET /api/v1/admins/myexams
    Return:
      - list of all admin's Exam objects as JSON represented
    """
    my_exams = db.get_my_exams(Exam, current_user.id)
    return jsonify(my_exams)