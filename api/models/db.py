#!/usr/bin/env python3
"""
Database Controller Module
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Database():
    """
        Database Class - perform action with db seamlessly
        Methods:
            create_model: create a model with specified args
            get: get a single model by specified args
            get_all: get all the model's data from the database
            get_page: get all data of model from the database as segments
            update: update a model
            delete: delete a model
    """
    def __init__(self):
        """ Initialize the database connection """
        self.db = SQLAlchemy(model_class=Base)
