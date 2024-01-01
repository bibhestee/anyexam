#!/usr/bin/env python3
"""
Initialize database
"""
from sqlalchemy import TIMESTAMP, UUID
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4


class Base(DeclarativeBase):
    def __tablename__(self):
        return self.__name__.lower()
    id = mapped_column(UUID, primary_key=True, default=uuid4)
    created_at = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())



db_engine = SQLAlchemy(model_class=Base)


