#!/usr/bin/env python3
"""
Database Controller Module
"""
from uuid import uuid4
from api.models import db_engine
db = db_engine


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
    def create_model(self, model, **kwargs):
        """ create a model """
        from api import app
        with app.app_context():
            try:
                id = str(uuid4())
                obj = model(**kwargs)
                obj.id = id
                db.session.add(obj)
                db.session.commit()
                return obj
            except Exception as e:
                db.session.rollback()
                return {
                    'error': e._message()
                }

    def get_model(self, model, id):
        """ get a single model """
        from api import app
        with app.app_context():
            return db.one_or_404(db.select(model).filter_by(id=id))