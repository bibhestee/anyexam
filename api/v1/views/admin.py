#!/usr/bin/env python3
"""
Admin Routes
"""
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from api.models.admin import Admin
from api.models.db import Database

bp  = Blueprint('admin', __name__, url_prefix='/api/v1/admins')
db = Database()


@bp.route('/<id>', methods=['GET'], strict_slashes=False)
def get_admin():
    """ get a single user """
    id = request.args.get('id')
    print(id)
    admin = db.get_model(Admin, id)
    print(admin)
    if admin:
        return jsonify({
            'status': 'success',
            'data': admin.to_json(),
            'message': 'Admin retrieved successfully'
        })
