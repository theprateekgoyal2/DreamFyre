from typing import Any
import logging
from sqlalchemy.exc import SQLAlchemyError
from extensions import bcrypt
from common.utils import send_email_to_user, generate_user_tokens, check_token_validity
from .validations import validate_user_data
from sql_config.utils import session_wrap
from .models import Users


@session_wrap
def register_user_handler(request_payload: dict, session: Any) -> dict:
    """
    Handles the registration of a new user. Validates input, creates a user, sends email if applicable,
    and returns access tokens.

    Args:
        request_payload (dict): The JSON payload containing user details.
        session (Any): The SQLAlchemy session.

    Returns:
        dict: A response dict containing a success message and tokens or an error.
    """
    try:
        name = request_payload.get('name')
        mobile = request_payload.get('mobile')
        email = request_payload.get('email')
        password = request_payload.get('password')

        # Validate input data
        validation_result = validate_user_data(name, password, email, mobile, False, session)
        if 'error' in validation_result:
            return validation_result

        # Create new user
        new_user = Users(
            name=name.capitalize(),
            password=password,
            mobile=mobile if mobile else None,
            email=email if email else None
        )

        session.add(new_user)
        session.commit()

        # Optional: Send welcome email
        if email:
            message = f'Hi {name.capitalize()}, Welcome to Fitness Club.'
            send_email_to_user(email, message)

        # Generate JWT tokens
        tokens = generate_user_tokens(new_user.prim_id)

        return {
            "message": "User created successfully. Please check your inbox.",
            "tokens": tokens
        }

    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Database error: {str(e)}")
        return {"error": "Database error", "message": str(e)}

    except Exception as e:
        session.rollback()
        logging.error(f"Unexpected error: {str(e)}")
        return {"error": "Unexpected error", "message": str(e)}


@session_wrap
def login_user_handler(request_payload: dict, headers: dict, session: Any) -> dict:
    """
    Handles user login by validating credentials, checking existing valid tokens,
    and generating new access/refresh tokens if needed.

    Args:
        request_payload (dict): The JSON payload with login credentials.
        headers (dict): The request headers, used to check for an existing token.
        session (Any): SQLAlchemy session from @session_wrap.

    Returns:
        dict: A success message with tokens or an error message.
    """
    try:
        name = request_payload.get('name')
        mobile = request_payload.get('mobile')
        email = request_payload.get('email')
        password = request_payload.get('password')

        # Validate login input
        validation_result = validate_user_data(name, password, email, mobile, True, session)
        if 'error' in validation_result:
            return validation_result

        # Fetch user by mobile or email
        user = Users.get_by_mobile(session, mobile) if mobile else Users.get_by_email(session, email)
        if not user:
            return {"error": "User not found"}

        # Validate password
        if not bcrypt.check_password_hash(user.password, password):
            return {"error": "Wrong password entered"}

        # Avoid generating token if existing one is valid
        if 'token' in headers:
            token_data = check_token_validity(headers['token'])
            if token_data:
                return token_data

        # Generate and return new tokens
        tokens = generate_user_tokens(user.prim_id)

        return {
            'message': f'You are successfully logged in as {user.name}',
            'tokens': tokens
        }

    except Exception as e:
        logging.error(f"Login error: {str(e)}")
        return {"error": "Login failed", "message": str(e)}
