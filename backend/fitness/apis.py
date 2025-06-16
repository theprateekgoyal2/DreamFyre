from flask import request
from .utils import get_fitness_classes, get_class_bookings_per_user, create_new_class, create_class_booking_per_user
from decorators import login_required


@login_required
def get_fitness_classes_api():
    class_name = request.args.get('class_name')
    if class_name:
        return get_fitness_classes(class_name)

    return {'error': 'Please enter a class name to search!'}


@login_required
def create_new_fitness_class_api():
    payload = request.get_json()
    return create_new_class(payload)


@login_required
def create_class_booking_per_user_api():
    token = request.headers['token']
    class_id = int(request.args.get('class_id'))

    return create_class_booking_per_user(token, class_id)


@login_required
def get_class_bookings_per_user_api():
    token = request.headers['token']

    return get_class_bookings_per_user(token)
