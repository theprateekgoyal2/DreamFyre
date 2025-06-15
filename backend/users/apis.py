from flask import request
from .utils import register_user_handler, login_user_handler


def register_user_api():
    request_body = request.get_json()

    return register_user_handler(request_body)


def login_user_api():
    request_body = request.get_json()
    headers = request.headers

    return login_user_handler(request_body, headers)
