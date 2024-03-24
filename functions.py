#!/usr/bin/python3
""" Other function will be here"""
from phonenumbers import parse, is_valid_number, phonenumberutil
from wtforms.validators import ValidationError



def validate_phone(form, field):
    """ Validates the client phone number """
    try:
        phone_no = parse(field.data)
        if not is_valid_number(phone_no):
            raise ValueError("Invalid phone number")
    except (phonenumberutil.NumberParseException, ValueError):
        raise ValidationError("Invalid phone number format")