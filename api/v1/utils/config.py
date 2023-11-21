#!/usr/bin/env python3
"""
Application configuration module
"""
from os import getenv


class Config():
    """
        Config - application configuration datas
        Attributes:
    """
    SECRET_KEY = getenv('SECRET_KEY', '$2b$10$YRC5u2X6K')
    usr = getenv('DB_USER', 'anyexam')
    host = getenv('DB_HOST','localhost')
    pwd = getenv('DB_PWD', 'anyexam')
    db = 'anyexam'
    SQLALCHEMY_DATABASE_URI = f'postgresql://{usr}:{pwd}@{host}/{db}'