#!/usr/bin/env python3
"""
Quiz Routes
"""
from flask import Blueprint, request, jsonify
# from api.models.admin import Admin
from api.models.db import Database
# from api.models.candidate import Candidate
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
