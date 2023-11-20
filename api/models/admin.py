#!/usr/bin/env python3
"""
Admin Model
"""
from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from api.models import db_engine

db = db_engine


class Admin(db.Model):
    """
        Admin Model
        Fields:
            id: Admin id
            fullname: Full name of the admin
            org_name: School or Organization name
            email: Email address of the admin
            password: Password of the admin
            position: Position of the admin
    """
    id: Mapped[Uuid] = mapped_column(Uuid, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String, nullable=False)
    lastname: Mapped[str] = mapped_column(String, nullable=False)
    organization: Mapped[str] = mapped_column(String, nullable=False)
    position: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)


    def to_json(cls):
        return {
            'id': cls.id,
            'email': cls.email,
            'firstname': cls.firstname,
            'lastname': cls.lastname,
            'organization': cls.organization,
            'position': cls.position
        }