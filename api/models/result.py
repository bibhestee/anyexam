#!/usr/bin/env python3
"""
Result Model
"""
from sqlalchemy import String, Uuid, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
    email: Mapped[str] = mapped_column(String, nullable=True)
    firstname: Mapped[str] = mapped_column(String, nullable=True)
    lastname: Mapped[str] = mapped_column(String, nullable=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    score: Mapped[str] = mapped_column(Integer, nullable=True)
    token_used: Mapped[bool] = mapped_column(Boolean, default=False)
    admin_id: Mapped[str] = mapped_column(Uuid, ForeignKey('admin.id'), nullable=False)
    exam_id: Mapped[str] = mapped_column(Uuid, ForeignKey('exam.id'), nullable=False)
    # One to many relationship
    exam: Mapped['Exam'] = relationship(back_populates='results')

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
            'created_at': str(cls.created_at),
            'updated_at': str(cls.updated_at)
        }