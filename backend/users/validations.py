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


def validate_user_data(
    name: str,
    password: str,
    email: str,
    mobile: str,
    login: bool,
    session: Any
) -> dict:
    """
    Validates user input for registration or login.

    Args:
        name (str): User's name.
        password (str): Password string.
        email (str): User's email address (optional if mobile is provided).
        mobile (str): User's mobile number (optional if email is provided).
        login (bool): Flag to determine if it's a login or registration validation.
        session (Any): SQLAlchemy session.

    Returns:
        dict: A dictionary containing either an error message or a success message.
    """

    def error(msg: str) -> dict:
        return {"error": msg}

    if not name or not name.strip():
        return error("Name is required")

    if not password or len(password) < 6:
        return error("Password must be at least 6 characters long")

    if not email and not mobile:
        return error("Either email address or mobile number is required")

    if email and not validate_email(email):
        return error("Please enter a valid email address")

    if mobile and not validate_number(f'+91{str(mobile)}'):
        return error("Invalid phone number format")

    if not login:
        # Registration flow: Check if user already exists
        if email and Users.get_by_email(session, email):
            return error("User with this email already exists, please login")

        if mobile and Users.get_by_mobile(session, mobile):
            return error("User with this mobile number already exists, please login")

    return {"message": "User validated successfully"}

