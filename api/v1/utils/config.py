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
    DB_USER = getenv('DB_USER')
    DB_HOST = getenv('DB_HOST')
    DB_PWD = getenv('DB_PWD')
    DB = getenv('DB')