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
    SECRET_KEY = getenv('SECRET_KEY')
    usr = getenv('DB_USER')
    host = getenv('DB_HOST')
    pwd = getenv('DB_PWD')
    db = getenv('DB')
    SQLALCHEMY_DB_URI = f'postgresql://{usr}:{pwd}@{host}/{db}'