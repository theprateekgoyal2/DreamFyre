import re
from typing import Any
import phonenumbers
from .models import Users


def validate_email(email: str) -> bool:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    if re.fullmatch(regex, email):
        return True
    return False


def validate_number(phone: str) -> bool:
    my_string_number = phone
    my_number = phonenumbers.parse(my_string_number)
    return phonenumbers.is_valid_number(my_number)


def validate_user_data(name: str, password: str, email: str, mobile: str, login: bool, session: Any) -> dict:
    if not name:
        return {"error": "Name is required"}

    if len(password) < 6:
        return {"error": "Password must be at least 6 characters long"}

    if not email and not mobile:
        return {"error": "Either email address or mobile number is required"}

    if email:
        if not validate_email(email):
            return {"error": "Please enter a valid email address"}

    if mobile:
        phone = f'+91{str(mobile)}'
        if not validate_number(phone):
            return {"error": "Invalid phone number"}

    if not login:
        if email:
            if Users.get_by_email(session, email):
                return {"error": "User with this email already exists, please login"}

        if mobile:
            if Users.get_by_mobile(session, mobile):
                return {"error": "User with this mobile number already exists, please login"}

    return {'message': 'User validated successfully'}
