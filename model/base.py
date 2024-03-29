#!/usr/bin/python3
"""Base models for other models"""

from datetime import datetime
from app import Base
from werkzeug.security import generate_password_hash
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Table
from sqlalchemy.orm import relationship



class BaseUser(Base):
    """The Base User for clients and plumbers"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    image_file = Column(String(20), nullable=False, default='default.jpg')
    password_hash = Column(String(60), nullable=False)
    date_joined = Column(DateTime, nullable=False, default=datetime.utcnow)
    phone_no = Column(Integer, unique=True, nullable=False)
    state = Column(String(20), nullable=False)
    
    def __repr__(self):
        """Returns the string representation of our BaseUser"""
        return f"BaseUser('{self.username}', '{self.email}', '{self.image_file}')"
    
    def set_password(self, password):
        """ Generate a password hash """
        self.password_hash = generate_password_hash(password)
    
    
class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    job_title = Column(String(100), nullable=False)
    content = Column(String(1000), nullable=False)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow)
    # Define a one-to-many relationship with Message model
    messages = relationship('Message', cascade='all, delete-orphan', backref='job')
    # Define a one-to-many relationship with Rank model
    ratings = relationship('Rank', cascade='all, delete-orphan', backref='job')
    
    
    def __repr__(self):
        return f"JobOffer('{self.job_title}', '{self.date_posted}')"
        
class Client(BaseUser):
    """ Clients models inheriting from BaseUser """
    __tablename__ = 'clients'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    jobs = relationship('Job', backref='client', lazy='dynamic')
    
    def __repr__(self):
        """ Returns the clients repr """
        return f"Client('{self.username}', '{self.email}', '{self.image_file}', '{self.phone_no}', '{self.state}')"
    
jobs_plumbers = Table('jobs_plumbers',
    Column('job_id', Integer, ForeignKey('jobs.id'), primary_key=True),
    Column('plumber_id', Integer, ForeignKey('plumbers.id'), primary_key=True)
)


class Plumber(BaseUser):
    """ Plumber models from Baseuser """
    __tablename__ = 'plumbers'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    jobs_assigned = relationship('Job', secondaryjoin='jobs_plumbers', backref='assigned_plumbers', lazy='dynamic')  # many-to-many relationship

    
    def __repr__(self):
        return f"Plumber('{self.username}', '{self.email}', '{self.service_areas}', '{self.phone_no}', '{self.service_areas}', '{self.state}', '{self.bio}')"

class Message(Base):
    """Message model for clients and plumbers"""
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    message = Column(Text, nullable=False)
    date_sent = Column(DateTime, nullable=False, default=datetime.utcnow)
    client_id = Column(Integer, ForeignKey('clients.id'))
    plumber_id = Column(Integer, ForeignKey('plumbers.id'))
    
    def __repr__(self):
        """Returns the string representation of Message"""
        return f"Message('{self.message}', '{self.date_sent}')"
    
class Rank(Base):
    """Ranking model for clients and plumbers"""
    __tablename__ = 'ranking'
    id = Column(Integer, primary_key=True)
    rating = Column(Float, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'))
    plumber_id = Column(Integer, ForeignKey('plumbers.id'))
    
    def __repr__(self):
        """Returns the string representation of Ranking"""
        return f"Ranking('{self.rating}')"