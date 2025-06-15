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
    try:
        name = request_payload.get('name')
        mobile = request_payload.get('mobile')
        email = request_payload.get('email')
        password = request_payload.get('password')

        validation_result = validate_user_data(name, password, email, mobile, False, session)
        if 'error' in validation_result:
            return validation_result

        # Create new user object
        if mobile:
            new_user = Users(name=name.capitalize(), password=password, mobile=mobile, email=None)
        else:
            new_user = Users(name=name.capitalize(), password=password, mobile=None, email=email)

        session.add(new_user)
        session.commit()
        if email:
            message = f'Hi {name.capitalize()},Welcome to Fitness Club.'
            send_email_to_user(email, message)

        # Generate access and refresh tokens
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
        logging.error(f"Unexpected error: {str(e)}")
        return {"error": "Unexpected error", "message": str(e)}


@session_wrap
def login_user_handler(request_payload: dict, headers: dict, session: Any) -> dict:
    try:
        name = request_payload.get('name')
        mobile = request_payload.get('mobile')
        email = request_payload.get('email')
        password = request_payload.get('password')

        validation_result = validate_user_data(name, password, email, mobile, True, session)
        if 'error' in validation_result:
            return validation_result

        if mobile:
            user = Users.get_by_mobile(session, mobile)
        else:
            user = Users.get_by_email(session, email)

        if bcrypt.check_password_hash(user.password, password):

            # This block will prevent from generating new token if the old one is still valid.
            if 'token' in headers:
                token_data = check_token_validity(headers['token'])
                if token_data:
                    return token_data

            # Generate access and refresh tokens
            tokens = generate_user_tokens(user.prim_id)

            return {
                    'message': f'You are successfully logged in as {user.name}',
                    'tokens': tokens
            }

        return {"error": "Wrong password entered"}

    except Exception as e:
        return {"error": str(e)}
