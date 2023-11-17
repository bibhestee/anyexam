#!/usr/bin/env python3
"""
Authentication Routes
"""
from flask import Blueprint

bp  = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@bp.route('/', strict_slashes=False)
def auth_main():
    """ home route """
    return 'Authentication home'