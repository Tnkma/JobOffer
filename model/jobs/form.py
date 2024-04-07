#!/usr/bin/python3
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

STATE_CHOICE = [
    ('Abia', 'Abia'),
    ('Adamawa', 'Adamawa'),
    ('Akwa Ibom', 'Akwa Ibom'),
    ('Anambra', 'Anambra'),
    ('Bauchi', 'Bauchi'),
    ('Bayelsa', 'Bayelsa'),
    ('Benue', 'Benue'),
    ('Borno', 'Borno'),
    ('Cross River', 'Cross River'),
    ('Delta', 'Delta'),
    ('Ebonyi', 'Ebonyi'),
    ('Edo', 'Edo'),
    ('Ekiti', 'Ekiti'),
    ('Enugu', 'Enugu'),
    ('FCT', 'FCT'),
    ('Gombe', 'Gombe'),
    ('Imo', 'Imo'),
    ('Jigawa', 'Jigawa'),
    ('Kaduna', 'Kaduna'),
    ('Kano', 'Kano'),
    ('Katsina', 'Katsina'),
    ('Kebbi', 'Kebbi'),
    ('Kogi', 'Kogi'),
    ('Kwara', 'Kwara'),
    ('Lagos', 'Lagos'),
    ('Nasarawa', 'Nasarawa'),
    ('Niger', 'Niger'),
    ('Ogun', 'Ogun'),
    ('Ondo', 'Ondo'),
    ('Osun', 'Osun'),
    ('Oyo', 'Oyo'),
    ('Plateau', 'Plateau'),
    ('Rivers', 'Rivers'),
    ('Sokoto', 'Sokoto'),
    ('Taraba', 'Taraba'),
    ('Yobe', 'Yobe'),
    ('Zamfara', 'Zamfara')
]


class PostJobForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    job_description = StringField('Job Description', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    state = SelectField('State', choices=STATE_CHOICE)
    submit = SubmitField('Post Job')
    
class RankForm(FlaskForm):
    rank = SelectField('Rank', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    submit = SubmitField('Rank')
    
class ApplyForm(FlaskForm):
    
    submit = SubmitField('Apply')