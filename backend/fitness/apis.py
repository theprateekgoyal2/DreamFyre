from flask import request
from decorators import login_required
from .utils import get_fitness_classes_handler, get_class_bookings_per_user_handler, create_new_fitness_class_handler, \
    create_class_booking_per_user_handler, cancel_user_class_booking_handler


@login_required
def get_fitness_classes_api():
    class_name = request.args.get('class_name')

    if not class_name or not isinstance(class_name, str):
        return {'error': 'Invalid or missing class name'}

    return get_fitness_classes_handler(class_name)


@login_required
def create_new_fitness_class_api():
    payload = request.get_json()
    return create_new_fitness_class_handler(payload)


@login_required
def create_class_booking_per_user_api():
    token = request.headers['token']
    class_id = int(request.args.get('class_id'))

    if not class_id:
        return {'error': 'class_id is required'}

    return create_class_booking_per_user_handler(token, class_id)


@login_required
def get_class_bookings_per_user_api():
    token = request.headers['token']

    return get_class_bookings_per_user_handler(token)


@login_required
def cancel_user_class_booking_api():
    token = request.headers['token']
    booking_id = int(request.args.get('booking_id'))

    if not booking_id:
        return {'error': 'booking_id is required'}

    return cancel_user_class_booking_handler(token, booking_id)
