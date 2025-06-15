from typing import Any
from sql_config import session_wrap
from decorators import login_required
from .models import FitnessClass, Bookings
from .validations import validate_fitness_class_payload
from users.models import Users
from constants import BookingStatus, FitnessClasses, Fitness_Class_Description_Mapper


@session_wrap
def create_new_class(request_body: dict, session: Any) -> dict:
    is_valid = validate_fitness_class_payload(request_body)
    if 'error' in is_valid:
        return is_valid

    name = request_body.get('name')
    capacity = request_body.get('capacity')
    instructor = request_body.get('instructor')
    duration = request_body.get('duration')
    datetime_str = request_body.get('datetime_str')

    description = Fitness_Class_Description_Mapper.get('name')

    new_class = FitnessClass.create_class(
        name.lower(), datetime_str, duration, instructor, capacity, description
    )

    session.add(new_class)
    session.commit()

    return {'message': 'New class created successfully', 'data': new_class.to_dict()}


@session_wrap
@login_required
def get_class_bookings_per_user(token: str, session: Any):
    user_id = Users.get_user_id(token, session)
    if not user_id:
        return {'error': 'No user found'}

    classes = session.query(Bookings).filter(client_id=user_id).all()

    return {item.to_dict() for item in classes}


@session_wrap
@login_required
def create_class_booking_per_user(token: str, class_id: int, session: Any):
    user_id = Users.get_user_id(token, session)
    if not user_id:
        return {'error': 'No user found'}

    try:
        fitness_class = FitnessClass.get_by_id(session, class_id, True, no_wait=True)
    except Exception as e:
        return {'error': f'Error booking class: {str(e)}'}

    if fitness_class.available_slots:
        fitness_class.available_slots -= 1

    else:
        return {'error': 'No slots available for this class.'}

    booking = Bookings.create_booking(class_id=class_id, client_id=user_id)
    booking.status = BookingStatus.CONFIRMED.value

    session.add(fitness_class)
    session.add(booking)

    session.commit()

    return {'message': 'success', 'data': booking.to_dict()}
