#!/usr/bin/env python3
"""
Examination Model
"""
from sqlalchemy import String, Integer, Uuid, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from api.models import db_engine
from api.models.result import Result
from typing import List

db = db_engine

class Exam(db.Model):
    """
        Exam Model - Examination condition model
        Fields:
            title: title of the exam.
            exam_type: type of the exam.
            duration: duration of the exam.
            no_of_questions: Number of question for the exam.
            results: Handle result's visibility to candidate.
    """
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    exam_type: Mapped[str] = mapped_column(String, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    no_of_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    result: Mapped[str] = mapped_column(Enum('visible', 'hidden', name='result_visibility'), default='visible')
    admin_id: Mapped[str] = mapped_column(Uuid, ForeignKey('admin.id'), nullable=False)
    # One to many - one exam have many results
    results: Mapped[List['Result']] = relationship(back_populates='exam', lazy='joined')
    # One to many - one admin have many exams
    admin: Mapped['Admin'] = relationship(back_populates='exams')

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise AssertionError('Exam title is required')
        if len(title) < 3 or len(title) > 40:
            raise AssertionError('title must be between 3 and 40 characters')
        return title
    
    @validates('exam_type')
    def validate_exam_type(self, key, exam_type):
        if not exam_type:
            raise AssertionError('Exam exam_type is required')
        if len(exam_type) < 2 or len(exam_type) > 15:
            raise AssertionError('exam_type must be between 2 and 15 characters')
        return exam_type
    
    @validates('no_of_questions')
    def validate_no_of_questions(self, key, no_of_questions):
        if not no_of_questions:
            raise AssertionError('no_of_questions is required')
        try:
            int(no_of_questions)
        except Exception:
            raise AssertionError('no_of_questions should be an integer')
        return no_of_questions

    @validates('duration')
    def validate_duration(self, key, duration):
        if not duration:
            raise AssertionError('duration is required')
        try:
            int(duration)
        except Exception:
            raise AssertionError('duration should be an integer')
        return duration
        
    def to_json(cls):
        return {
            'exam_id': str(cls.id),
            'admin_id': str(cls.admin_id),
            'title': cls.title,
            'exam_type': cls.exam_type,
            'no_of_questions': cls.no_of_questions,
            'duration': cls.duration,
            'result': cls.result,
            'created_at': str(cls.created_at),
            'updated_at': str(cls.updated_at),
            'results': [result.to_json() for result in cls.results]
        }
