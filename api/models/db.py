#!/usr/bin/env python3
"""
Database Controller Module
"""
from flask import abort
from api.models import db_engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import IntegrityError

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
                obj = model(**kwargs)
                db.session.add(obj)
                db.session.commit()
                return obj.to_json()
            except IntegrityError as e:
                db.session.rollback()
                raise ValueError(e._message())

    def get_model(self, model, id: str):
        """ get a single model """
        from api import app
        with app.app_context():
            try:
                # Alternate statement of one_or_404
                statement = db.select(model).filter_by(id=id)
                # unique is used for joined lazy loading (one to many relationship)
                return db.session.execute(statement).unique().scalar_one()
            except (NoResultFound, MultipleResultsFound):
                abort(404)

    def get_all(self, model):
        """ get all model """
        from api import app
        with app.app_context():
            statement = db.select(model)
            objs = db.session.execute(statement).unique().all()
            return [obj[0].to_json() for obj in objs]

    def get_my_exams(self, model, admin_id):
        """ get all my exam model """
        from api import app
        with app.app_context():
            statement = db.select(model).filter_by(admin_id=admin_id)
            objs = db.session.execute(statement).unique().all()
            return [obj[0].to_json() for obj in objs]
        
    def get_exam_results(self, model, exam_id: str):
        """ get all results related to exam_id """
        from api import app
        with app.app_context():
            statement = db.select(model).filter_by(exam_id=exam_id)
            objs = db.session.execute(statement).unique().all()
            return [obj[0].to_json() for obj in objs]
        
    def update(self, model, id: str,  **kwargs) -> None:
        """ Update model with arbitrary keyword arguments """
        try:
            obj = self.get_model(model, id)
            for k, v in kwargs.items():
                if hasattr(model, k):
                    setattr(obj, k, v)
                else:
                    raise AttributeError
            from api import app
            with app.app_context():
                db.session.merge(obj)
                db.session.commit()
                return obj
        except NoResultFound:
            raise ValueError
    
    def delete(self, obj):
        """ delete model """
        from api import app
        with app.app_context():
            db.session.delete(obj)
            db.session.commit()