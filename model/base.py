#!/usr/bin/python3
"""Base models for other models"""
from datetime import datetime
from model import Base
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Table, MetaData, Boolean
from sqlalchemy.orm import relationship

metadata = MetaData()

class BaseUser(Base, UserMixin):
    """The Base User for clients and plumbers"""
    # __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    image_file = Column(String(20), nullable=False, default='default.jpg')
    password = Column(String(60), nullable=False)
    date_joined = Column(DateTime, nullable=False, default=datetime.utcnow)
    phone = Column(String(14), nullable=False)
    state = Column(String(20), nullable=False)
    
    def __repr__(self):
        """Returns the string representation of our BaseUser"""
        return f"BaseUser('{self.username}', '{self.email}', '{self.image_file}')"
        
    def get_id(self):
        """ Returns the User_id (primary key)"""
        return self.id

class JobPlumber(Base):
    __tablename__ = 'job_plumbers'
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'))
    plumber_id = Column(Integer, ForeignKey('plumbers.id'))
    is_assigned = Column(Boolean, default=True)
    
    plumber = relationship('Plumber', backref='job_plumbers')
    job = relationship('Job', backref='job_plumbers')
    
class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    job_title = Column(String(50), nullable=False)
    job_description = Column(String(100), nullable=False)
    completed = Column(Boolean, default=False)
    content = Column(String(1000), nullable=False)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow)
    location = Column(String(100), nullable=False)
    
    # Relationship between jobs and clients
    client_id = Column(Integer, ForeignKey('clients.id'))

    
    def __repr__(self):
        return f"Job('{self.job_title}', '{self.date_posted}', '{self.client_id}', '{self.content}', '{self.location}'), '{self.job_description}'"


class Plumber(BaseUser):
    """ Plumber models from Baseuser """
    __tablename__ = 'plumbers'
    id = Column(Integer, ForeignKey('base_user.id'), primary_key=True)
    bio = Column(Text, nullable=True)
    # service_areas = Column(String(100), nullable=True)
    
    def __init__(self, username, email, phone, state, password):
        super().__init__(username=username, email=email, phone=phone, state=state, password=password)
        
    
    def __repr__(self):
        return f"Plumber('{self.username}', '{self.email}', '{self.phone}', '{self.state}', '{self.image_file}'"

   
class Client(BaseUser):
    """ Clients models inheriting from BaseUser """
    __tablename__ = 'clients'
    id = Column(Integer, ForeignKey('base_user.id'), primary_key=True)
    jobs = relationship('Job', backref="clients")
    
    def __init__(self, username, email, phone, state, password):
        super().__init__(username=username, email=email, phone=phone, state=state, password=password)
        
    
    def __repr__(self):
        """ Returns the clients repr """
        return f"Client('{self.username}', '{self.email}', '{self.image_file}', '{self.phone}', '{self.state}')"
