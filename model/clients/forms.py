#!/usr/bin/python3

from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from phonenumbers import parse, is_valid_number, national_significant_number, NumberParseException
from flask_wtf import FlaskForm
from model.base import Client
from flask_login import current_user

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


def validate_phone(form, field):
    """ Validates the client phone number and stores it with +234 prefix """
    client = Client.query.filter_by(phone=field.data).first()
    if client and client.id != getattr(form, 'obj_id', None):
        raise ValidationError('This phone number already exists. Please choose a different one.')

    try:
        parsed_phone = parse(field.data, "NG")  # Parse the phone number with country code "NG" for Nigeria
        if not is_valid_number(parsed_phone):
            raise ValueError("Invalid phone number")

        # Extract the national significant number
        significant_number = national_significant_number(parsed_phone)
        # Prepend +234 country code
        phone_number_with_country_code = f'+234{significant_number}'
        # Update the field value with the formatted number
        field.data = phone_number_with_country_code
        return True

    except NumberParseException:
        raise ValidationError("Invalid phone number format")
    except ValueError:
        raise ValidationError("Invalid phone number")


class RegistrationForm(FlaskForm):    
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone Number (+234)', validators=[validate_phone, DataRequired()])
    state = SelectField('State', choices=STATE_CHOICE)
    submit = SubmitField('Sign Up')
    
    
    
    def validate_email(self, email):
        """ Validates the username """
        email = Client.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('This email already exist. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number (+234)', validators=[validate_phone, DataRequired()])
    state = SelectField('State', choices=STATE_CHOICE)
    submit = SubmitField('Update Account')
    
    def validate_email(self, email):
        """ Validates the username """
        if email.data != current_user.email:
            email = Client.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('This email already exist. Please choose a different one.')
            
            
            
            
class SelectState(FlaskForm):
    state = SelectField('State', choices=STATE_CHOICE)
    submit = SubmitField('Select State')