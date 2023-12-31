#!/usr/bin/env python3
"""
Admin Model
"""
from sqlalchemy import String
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
import re
from api.models import db_engine
from api.models.exam import Exam

db = db_engine


class Admin(db.Model):
    """
        Admin Model
        Fields:
            fullname: Full name of the admin
            org_name: School or Organization name
            email: Email address of the admin
            password: Password of the admin
            position: Position of the admin
    """
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String, nullable=False)
    lastname: Mapped[str] = mapped_column(String, nullable=False)
    organization: Mapped[str] = mapped_column(String, nullable=False)
    position: Mapped[str] = mapped_column(db.Enum('leader', 'staff', name='admin_position'), default='staff')
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    answer: Mapped[str] = mapped_column(String, nullable=True)
    # candidate: Mapped[str] = relationship('Candidate', backref='candidate', lazy=True)
    # One to many relationship with exam
    exams: Mapped[List['Exam']] = relationship(back_populates='admin', lazy='joined')

    @validates('firstname') 
    def validate_firstname(self, key, firstname):
        if not firstname:
            raise AssertionError('No firstname provided')
        if len(firstname) < 3 or len(firstname) > 20:
            raise AssertionError('firstname must be between 3 and 20 characters') 
        return firstname 
    
    @validates('lastname') 
    def validate_lastname(self, key, lastname):
        if not lastname:
            raise AssertionError('No lastname provided')
        if len(lastname) < 3 or len(lastname) > 20:
            raise AssertionError('lastname must be between 3 and 20 characters') 
        return lastname 
    
    @validates('organization') 
    def validate_organization(self, key, organization):
        if not organization:
            raise AssertionError('No organization name provided')
        if len(organization) < 3 or len(organization) > 20:
            raise AssertionError('organization name must be between 3 and 20 characters') 
        return organization 

    @validates('answer') 
    def validate_answer(self, key, answer):
        if not answer:
            raise AssertionError('No answer provided. What is your favourite city?')
        if len(answer) < 3 or len(answer) > 20:
            raise AssertionError('answer name must be between 3 and 20 characters') 
        return answer
    
    @validates('position') 
    def validate_position(self, key, position):
        if position and position not in ['leader', 'staff']:
            raise AssertionError('position must be leader or staff') 
        return position 
    
    @validates('email') 
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('No email provided')
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError('Provided email is not an email address')
        return email
        
    def to_json(cls):
        return {
            'admin_id': str(cls.id),
            'email': cls.email,
            'firstname': cls.firstname,
            'lastname': cls.lastname,
            'organization': cls.organization,
            'position': cls.position,
            'created_at': str(cls.created_at),
            'updated_at': str(cls.updated_at),
            'exams': [exam.to_json() for exam in cls.exams]
        }