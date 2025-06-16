from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import decode_token
import jwt
from sql_config import session_wrap
from users.models import Users


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = ''

        if 'token' in request.headers:
            token = request.headers['token']

        if not token:
            return {'message': 'Token is missing !!'}

        try:

            # Fetch user from the database using public_id
            current_user_id = get_user_id_from_token(token=token)

            if not current_user_id:
                return {'message': 'User not found'}

            # Pass the current user to the decorated function
            return f(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired !!'}), 401

        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token !!'}), 401

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return decorated


@session_wrap
def get_user_id_from_token(token, session):
    data = decode_token(token)
    current_user = session.query(Users).filter_by(prim_id=data['sub']).first()
    return current_user.prim_id if current_user else None
