#!/usr/bin/env python3
"""
Password validator
"""
import re
from werkzeug.security import generate_password_hash


def hash_password(password: str) -> bytes:
    """ check password and hash it """
    if not password:
        raise AssertionError('Password not provided')
    if type(password) != str:
        raise AssertionError('Invalid parameter type for password')
    if not re.match('\d.*[A-Z]|[A-Z].*\d', password):
        raise AssertionError('Password must contain at least 1 capital letter and 1 number')
    if len(password) < 8 or len(password) > 50:
        raise AssertionError('Password must be between 8 and 50 characters')
    return generate_password_hash(password)