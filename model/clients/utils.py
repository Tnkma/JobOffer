#!/usr/bin/python3
"""Base models for other models"""
from model import db


def new(obj):
    """ Add the object to the current session """
    db.session.add(obj)

def save():
    """ Save the current session """
    db.session.commit()
    
def get_single(model, **kwargs):
    """ Get a single object from the database """
    return db.session.query(model).filter_by(**kwargs).first()

def get_all(model):
    """ Get all objects from the database """
    return db.session.query(model).all()

def delete(obj):
    """ Delete the object from the database """
    db.session.delete(obj)
    db.session.commit()
    
def query_first(cls):
    """ Query the first object """
    return db.session.query(cls).first()
    
