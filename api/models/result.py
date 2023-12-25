#!/usr/bin/env python3
"""
Result Model
"""
from sqlalchemy import String, Uuid, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, validates
import re
from api.models import db_engine

db = db_engine


class Result(db.Model):
    """
        Result model for candidates
        Fields:
            firstname: first name of the candidate
            lastname: last name of the candidate
            email: Email address of the candidate
            token: candidate token to access the exam
            score: candidate's score
            admin_id: Admin's id
            exam_id: associated exam id
            token_used: Boolean value to determine if token is used
    """
    email: Mapped[str] = mapped_column(String, unique=True)
    firstname: Mapped[str] = mapped_column(String)
    lastname: Mapped[str] = mapped_column(String)
    token: Mapped[str] = mapped_column(String, nullable=False)
    score: Mapped[str] = mapped_column(Integer)
    token_used: Mapped[bool] = mapped_column(Boolean, default=False)
    admin_id: Mapped[str] = mapped_column(Uuid, ForeignKey('admin.id'), nullable=False)
    exam_id: Mapped[str] = mapped_column(Uuid, ForeignKey('exam.id'), nullable=False)


    @validates('email')
    def validate_email(self, key, email):
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError('Provided email is not a valid email address')
        return email
    
    @validates('firstname')
    def validate_firstname(self, key, firstname):
        if len(firstname) < 2 or len(firstname) > 20:
            raise AssertionError('firstname must be between 2 and 20 characters')
        return firstname
        
    @validates('lastname')
    def validate_lastname(self, key, lastname):
        if len(lastname) < 2 or len(lastname) > 20:
            raise AssertionError('lastname must be between 2 and 20 characters')
        return lastname
    
    def to_json(cls):
        return {
            'result_id': str(cls.id),
            'admin_id': str(cls.admin_id),
            'exam_id': str(cls.exam_id),
            'email': cls.email,
            'firstname': cls.firstname,
            'lastname': cls.lastname,
            'token': cls.token,
            'score': cls.score,
            'token_used': cls.token_used,
            'created_at': str(cls.created_at)
        }