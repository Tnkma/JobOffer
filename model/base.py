#!/usr/bin/python3
"""Base models for other models"""
from datetime import datetime
from model import Base
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Table, MetaData
from sqlalchemy.orm import relationship

# metadata = MetaData()


class BaseUser(Base, UserMixin):
    """The Base User for clients and plumbers"""
    # __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    image_file = Column(String(20), nullable=False, default='default.jpg')
    password = Column(String(60), nullable=False)
    date_joined = Column(DateTime, nullable=False, default=datetime.utcnow)
    phone = Column(String(14), unique=True, nullable=False)
    state = Column(String(20), nullable=False)
    
    def __repr__(self):
        """Returns the string representation of our BaseUser"""
        return f"BaseUser('{self.username}', '{self.email}', '{self.image_file}')"
        
    def get_id(self):
        """ Returns the User_id (primary key)"""
        return self.id

    
class Plumber(BaseUser):
    """ Plumber models from Baseuser """
    __tablename__ = 'plumbers'
    id = Column(Integer, ForeignKey('base_user.id'), primary_key=True)
    # bio = Column(Text, nullable=True)
    # service_areas = Column(String(100), nullable=True)
    
    completed_jobs = relationship('Job', backref="plumbers")
    
    message = relationship('Message', backref='plumber_message')
    rank = relationship('Rank', backref='plumber_rank')
    
    def __init__(self, username, email, phone, state, password):
        super().__init__(username=username, email=email, phone=phone, state=state, password=password)
        
    def __str__(self):
        return f"Plumber('{self.username}', '{self.email}', '{self.phone}', '{self.state}', '{self.image_file}'"

    
    def __repr__(self):
        return f"Plumber('{self.username}', '{self.email}', '{self.phone}', '{self.state}', '{self.image_file}'"

    
    
class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    
    client_id = Column(Integer, ForeignKey('clients.id'))
    
    job_title = Column(String(100), nullable=False)
    job_description = Column(String(500), nullable=False)
    
    plumber_id = Column(Integer, ForeignKey('plumbers.id'))
    
    content = Column(String(1000), nullable=False)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow)
    location = Column(String(100), nullable=False)
    rank = relationship('Rank', backref='job_rank')
    # applicants = relationship('Plumber', secondary='applications', backref='jobs_applied')

    
    def __str__(self):
        return f"Job('{self.job_title}', '{self.date_posted}', '{self.client_id}', '{self.content}', '{self.location}'), '{self.plumber_id}', '{self.job_description}'"
    
    
    def __repr__(self):
        return f"Job('{self.job_title}', '{self.date_posted}', '{self.client_id}', '{self.content}', '{self.location}'), '{self.plumber_id}', '{self.job_description}'"
        
class Client(BaseUser):
    """ Clients models inheriting from BaseUser """
    __tablename__ = 'clients'
    id = Column(Integer, ForeignKey('base_user.id'), primary_key=True)
    jobs = relationship('Job', backref="clients")
    # completed_jobs = relationship('Job', backref='completed_job')
    message = relationship('Message', backref='client_message')
    rank = relationship('Rank', backref='client_rank')
    
    def __init__(self, username, email, phone, state, password):
        super().__init__(username=username, email=email, phone=phone, state=state, password=password)
        
    def __str__(self):
        """ Returns the clients str """
        return f"Client('{self.username}', '{self.email}', '{self.image_file}', '{self.phone}', '{self.state}')"
    
    def __repr__(self):
        """ Returns the clients repr """
        return f"Client('{self.username}', '{self.email}', '{self.image_file}', '{self.phone}', '{self.state}')"
    
     
# jobs_plumbers = Table('jobs_plumbers', metadata,
    # Column('job_id', Integer, ForeignKey('jobs.id'), primary_key=True),
    # Column('plumber_id', Integer, ForeignKey('plumbers.id'), primary_key=True))


class Message(Base):
    """Model for message exchange between clients and plumbers"""
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    message = Column(Text, nullable=False)
    date_sent = Column(DateTime, nullable=False, default=datetime.utcnow)
    client_id = Column(Integer, ForeignKey('clients.id'))
    plumber_id = Column(Integer, ForeignKey('plumbers.id'))
    
    
    def __str__(self):
        """Returns the string representation of Message"""
        return f"Message('{self.message}', '{self.date_sent}', '{self.client_id}', '{self.plumber_id}')"
    
    def __repr__(self):
        """Returns the string representation of Message"""
        return f"Message('{self.message}', '{self.date_sent}', '{self.client_id}', '{self.plumber_id}')"
    
class Rank(Base):
    """Ranking model for clients and plumbers"""
    __tablename__ = 'ranking'
    id = Column(Integer, primary_key=True)
    rating = Column(Float, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'))
    plumber_id = Column(Integer, ForeignKey('plumbers.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))
    
    def __repr__(self):
        """Returns the string representation of Ranking"""
        return f"Ranking('{self.rating}', '{self.client_id}', '{self.plumber_id}')"
    
    def __str__(self):
        """Returns the string representation of Ranking"""
        return f"Ranking('{self.rating}', '{self.client_id}', '{self.plumber_id}')"
    
    
#class Application(Base):
    #""" Model for job applications """
    #__tablename__ = 'applications'
   # user_id = Column(Integer, ForeignKey('plumbers.id'), primary_key=True)
    #job_id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)
