#!/usr/bin/env python3
"""
Candidate Model
"""
from sqlalchemy import String, Uuid, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, validates
import re
from api.models import db_engine

db = db_engine


class Candidate(db.Model):
    """
        Model for Admin to register Candidate
        Fields:
            firstname: first name of the candidate
            lastname: last name of the candidate
            email: Email address of the candidate
    """
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String, nullable=False)
    lastname: Mapped[str] = mapped_column(String, nullable=False)
    admin_id: Mapped[str] = mapped_column(Uuid, ForeignKey('admin.id'), nullable=False)

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('No email provided')
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError('Provided email is not a valid email address')
        return email
    
    @validates('firstname')
    def validate_firstname(self, key, firstname):
        if not firstname:
            raise AssertionError('No firstname provided')
        if len(firstname) < 2 or len(firstname) > 20:
            raise AssertionError('firstname must be between 2 and 20 characters')
        return firstname
        
    @validates('lastname')
    def validate_lastname(self, key, lastname):
        if not lastname:
            raise AssertionError('No lastname provided')
        if len(lastname) < 2 or len(lastname) > 20:
            raise AssertionError('lastname must be between 2 and 20 characters')
        return lastname
    
    def to_json(cls):
        return {
            'candidate_id': str(cls.id),
            'admin_id': str(cls.admin_id),
            'email': cls.email,
            'firstname': cls.firstname,
            'lastname': cls.lastname,
            'created_at': str(cls.created_at)
        }