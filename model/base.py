#!/usr/bin/python3
"""Base models for other models"""

from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship


class BaseUser(db.Model):
    """The Base User for clients and plumbers"""
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(80), unique=True, nullable=False)
    email = db.Column(String(120), unique=True, nullable=False)
    image_file = db.Column(String(20), nullable=False, default='default.jpg')
    password_hash = db.Column(String(60), nullable=False)
    date_joined = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    phone_no = db.Column(Integer, unique=True, nullable=False)
    state = db.Column(String(20), nullable=False)
    
    def __repr__(self):
        """Returns the string representation of our BaseUser"""
        return f"BaseUser('{self.username}', '{self.email}', '{self.image_file}')"
    
    def set_password(self, password):
        """ Generate a password hash """
        self.password_hash = generate_password_hash(password)
    
    
    def check_password(self, password):
        """ Checks the password hash """
        return check_password_hash(self.password_hash, password)   
    
class JobOffer(db.Model):
    """This model will contain job_offers posted by clients"""
    __tablename__ = 'job_offer'
    id = db.Column(Integer, primary_key=True)
    job_title = db.Column(String(100), nullable=False)
    content = db.Column(String(1000), nullable=False)
    date_posted = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    client_id = db.relationship("Client", backref="job_offer")
    plumber_id = db.relationship("Plumber", backref="job_offer")
    # client = relationship("Client", foreign_keys=[client_id])
    # plumber = relationship("Client", foreign_keys=[plumber_id])
    
    def __repr__(self):
        """Returns the string representation of JobOffer"""
        return f"JobOffer('{self.job_title}', '{self.date_posted}')"
    
class Client(BaseUser):
    """ Clients models inheriting from BaseUser """
    __tablename__ = 'client'
    client_id = db.Column(Integer, ForeignKey('job_offer.id'), nullable=False)
    
    def __repr__(self):
        """ Returns the clients repr """
        return f"Client('{self.username}', '{self.email}', '{self.image_file}', '{self.phone_no}', '{self.state}')"


class Plumber(BaseUser):
    """ Plumber models from Baseuser """
    __tablename__ = 'plumber'
    service_areas = db.Column(String, nullable=True)
    average_rating = db.Column(Float, nullable=True)
    bio = db.Column(Text, nullable=True)
    plumber_id = db.Column(Integer, ForeignKey('job_offer.id'), nullable=False)

    def __repr__(self):
        return f"Plumber('{self.username}', '{self.email}', '{self.service_areas}', '{self.phone_no}', '{self.service_areas}', '{self.state}', '{self.bio})"
    
class Rating(db.Model):
    """ This model will contain ratings for plumbers """
    __tablename__ = 'rating'
    id = db.Column(Integer, primary_key=True)
    rating = db.Column(Integer, nullable=False)
    date_rated = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    client_id = db.Column(Integer, ForeignKey('client.id'), nullable=False)
    plumber_id = db.Column(Integer, ForeignKey('plumber.id'), nullable=False)
    
    def __repr__(self):
        """ Returns the string representation of Rating """
        return f"Rating('{self.rating}', '{self.date_rated}')"
    
class Message(db.Model):
    """ This model will contain messages between clients and plumbers """
    __tablename__ = 'message'
    id = db.Column(Integer, primary_key=True)
    message = db.Column(Text, nullable=False)
    date_sent = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    client_id = db.Column(Integer, ForeignKey('client.id'), nullable=False)
    plumber_id = db.Column(Integer, ForeignKey('plumber.id'), nullable=False)
    
    def __repr__(self):
        """ Returns the string representation of Message """
        return f"Message('{self.message}', '{self.date_sent}')"