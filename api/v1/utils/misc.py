#!/usr/bin/env python3
"""
Miscellenous Functions
"""
from uuid import uuid4


def generate_uuid():
    """ generate uuid """
    return str(uuid4())


def generate_candidate_token():
    """ generate candidate token """
    return generate_uuid()[:8]