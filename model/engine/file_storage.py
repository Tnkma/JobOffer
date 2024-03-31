#!/usr/bin/python3
""" Storage Class for the database """
from . import Client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.base import classes
from flask import current_app
from flask_sqlalchemy import SQLAlchemy  # Import Flask-SQLAlchemy

class DataStorage:
    """ Interacts with our database """
    __engine = None

    def __init__(self):
        """ Instantiate the data storage object """
        db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
        self.__engine = create_engine(db_uri)
        # Use Flask-SQLAlchemy to create sessionmaker
        self.__session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)

    def all(self, cls=None):
        """ Returns a list of all objects of a specific class or all Clients """
        if cls is None:
            return self.__session_factory.query(Client).all()
        if cls not in classes.values():
            return None
        return self.__session_factory.query(cls).all()

    def add_new(self, obj):
        """ Add the object to the current database session """
        self.__session_factory.session.add(obj)

    def db_commit(self):
        """ Commit the changes to the database """
        self.__session_factory.session.commit()

    def delete(self, obj=None):
        """ Deletes an object from the current database session """
        if obj is not None:
            self.__session_factory.session.delete(obj)

    def get(self, cls, id):
        """ Gets the object based on class name and id or None if not found """
        if cls not in classes.values():
            return None
        return self.__session_factory.query(cls).get(id)

    # Consider if the reload method is necessary in your application
    # def reload(self):
       # """ Reloads data from the database (use with caution) """
        #Base.metadata.create_all(self.__engine)
