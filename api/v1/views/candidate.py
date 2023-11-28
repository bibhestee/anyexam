#!/usr/bin/env python3
"""
Candidate Routes
"""
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.exc import DataError
from api.models.candidate import Candidate
from api.models.admin import Admin
from api.models.db import Database
from api.v1.utils.token_required import token_required


bp = Blueprint('candidate', __name__, url_prefix='/api/v1/candidate')
db = Database()

# dummy data
# users = [
#     {
#         'id': 12345312
#         'admin_id': 232423423,
#         'email': 'resd@swe.com',
#         'firstname': 'Tim',
#         'lastname': 'Joe',
#         'created_at': 10-12-2023
#     },
#     {
#         'id': 42345312
#         'admin_id': 432423423,
#         'email': 'tresd@swe.com',
#         'firstname': 'Timothy',
#         'lastname': 'Doe',
#         'created_at': 11-12-2023
#     }
# ]


# method not tested
@bp.route('/<candidate_id>', methods=['GET'], strict_slashes=False)
def get_one_candidate(candidate_id: str = None) -> str:
    """ GET /api/v1/candidate/:candidate_id
        Path parameter:
        - Candidate ID
        Return:
        - Candidate object JSON represented
        - 404 if the Candidate ID doesn't exist
    """
    if not candidate_id:
        abort(404)
    try:
        candidate = db.get_model(Candidate, candidate_id)
        if not candidate:
            abort(404)
    except DataError:
        abort(404)
    return jsonify({
        'status': 'success',
        'data': candidate.to_json(),
        'message': 'Candidate retrieved successfully'
    })


@bp.route('/', methods=['GET'], strict_slashes=False)
def view_all_candidates() -> str:
    """ GET /api/v1/candidate
    Return:
      - list of all Candidate objects JSON represented
    """
    all_candidates = db.get_all(Candidate)
    return jsonify(all_candidates)

@bp.route('/candidate_id', methods=['PUT'], strict_slashes=False)
@token_required
def update_candidate(current_user, candidate_id: str = None) -> str:
    """ PUT /api/v1/candidate/:id
    Path parameter:
      - candidate ID
    JSON body:
      - first_name (optional)
      - last_name (optional)
      - email (optional)
    Return:
      - candidate object JSON represented
      - 404 if the candidate ID doesn't exist
      - 400 if can't update the candidate
    """
    if not candidate_id:
        abort(404)
    data = request.get_json()
    if not data:
        payload = {
            'status': 'error',
            'message': 'Wrong format: check the request data'
        }
        return jsonify(payload), 400
    try:
        updatedModel = db.update(Candidate, candidate_id, **data)
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

@bp.route('/candidate_id', methods=['DELETE'], strict_slashes=False)
def delete_candidate(candidate_id: str = None) -> str:
    """ DELETE /api/v1/candidate/:id
    Path parameter:
      - candidate ID
    Return:
      - empty JSON if the candidate has been correctly deleted
      - 404 if the admin ID doesn't exist
    """
    if not candidate_id:
        abort(404)
    try:
        candidate = db.get_model(Candidate, candidate_id)
        if not candidate:
            abort(404)
    except DataError:
        error(404)
    db.delete(candidate)
    return jsonify({}), 204
