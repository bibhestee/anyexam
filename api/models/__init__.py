#!/usr/bin/env python3
"""
Initialize database
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db_engine = SQLAlchemy(model_class=Base)