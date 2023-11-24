#!/usr/bin/env python3
"""
Miscellenous Functions
"""
from uuid import uuid4


def generate_uuid() -> uuid:
    """ generate uuid """
    return str(uuid4())
