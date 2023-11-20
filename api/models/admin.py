#!/usr/bin/env python3
"""
Admin Model
"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from api.models import db_engine
# from flask_validator import ValidateInteger, ValidateString, ValidateEmail

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
    position: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)


    # @classmethod
    # def __declare_last__(cls):
    #     ValidateString(Admin.firstname)
    #     ValidateString(Admin.lastname)
    #     ValidateString(Admin.organization)
    #     ValidateString(Admin.position)
    #     ValidateEmail(Admin.email)
        
    def to_json(cls):
        return {
            'id': str(cls.id),
            'email': cls.email,
            'firstname': cls.firstname,
            'lastname': cls.lastname,
            'organization': cls.organization,
            'position': cls.position,
            'created_at': str(cls.created_at),
            'updated_at': str(cls.updated_at)
        }