#!/usr/bin/python3
""" Storage Class for the database """
from model.base import BaseUser, JobOffer, Base
from model.base import Client, Plumber
import models
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from model import classes
from flask import current_app

class DataStorage:
    """ Interacts with our mysql database """
    __engine = None
    __session = None
    
    def __init__(self):
        """ instatiate the datastorage object """
        db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
        self.__engine = create_engine(db_uri)
        Base.metadata.drop_all(self.__engine)
    
    def all(self, cls=None):
        """ Returns a dictionary of all the objects in the database """
        if cls is None:
            return self.__session.query(Client).all()
        if cls not in classes.values():
            return None
        all_cls = models.storage.all(cls)
        return all_cls
    
    
    def add_new(self, obj):
        """ Add the object to the current database session """
        self.__session.add(obj)
    
    def commit_db(self):
        """ commit the changes to the database """
        self.__session.commit()
        
    def delete(self, obj=None):
        """ Deletes from the current database seesion """
        if obj is not None:
            self.__session.delete()
            
    def reload(self):
        """ Reloads data from the database """
        Base.metadata.create_all(self.__engine)
        sessions = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sessions)
        self.__session = Session
        
    def close(self):
        """ calls remove method on the private session """
        self.__session.remove()
        
    def get(self, cls, id):
        """ Gets the object based on class name and id or None if not found """
        if cls not in classes.values():
            return None
        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value
        return None