#!/usr/bin/python3
""" Defines both plumbers and clients models here """
from model import BaseUser
from sqlalchemy import Column, String, Float, Text, relationship


class Client(BaseUser):
    """ Clients models inheriting from BaseUser """
    jobs = relationship('JobOffer', backref='client', lazy='dynamic')

    
    def __repr__(self):
        """ Returns the clients repr """
        return f"Client('{self.username}', '{self.email}', '{self.image_file}', '{self.phone_no}', '{self.state}')"


class Plumber(BaseUser):
    """ Plumber models from Baseuser """
    service_areas = db.Column(String, nullable=True)
    average_rating = db.Column(Float, nullable=True)
    bio = db.Column(Text, nullable=True)

    def __repr__(self):
        return f"Plumber('{self.username}', '{self.email}', '{self.service_areas}', '{self.phone_no}',
    '{self.service_areas}', '{self.state}', '{self.bio})"