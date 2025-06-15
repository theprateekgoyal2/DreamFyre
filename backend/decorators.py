from functools import wraps
from flask import request, jsonify
from users.models import Users
from flask_jwt_extended import decode_token
import jwt


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = ''

        if 'token' in request.headers:
            token = request.headers['token']

        if not token:
            return {'message': 'Token is missing !!'}

        try:
            # Decoding the payload to fetch the stored details
            data = decode_token(token)

            # Fetch user from the database using public_id
            current_user = Users.query.filter_by(prim_id=data['sub']).first()

            if not current_user:
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
