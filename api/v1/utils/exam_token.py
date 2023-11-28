#!/usr/bin/env python3
from uuid import uuid4


def generate_candidate_token(title: str) -> str:
    """ generate candidate token """
    uuid = uuid4()
    title = [word[0] for word in title.split(' ')]
    mnemo = ''.join(title).upper()
    return f"{mnemo}-{uuid}"
