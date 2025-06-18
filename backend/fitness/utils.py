import logging
from typing import Any
from sql_config import session_wrap
from users.models import Users
from .models import FitnessClass, Bookings
from .validations import validate_fitness_class_payload
from .constants import BookingStatus, FitnessClassDescriptionMapper


@session_wrap
def get_fitness_classes_handler(class_name: str, session: Any) -> dict:
    """
    Fetches all upcoming fitness classes by class name.

    Args:
        class_name (str): The name of the fitness class (e.g., 'zumba', 'yoga').
        session (Any): SQLAlchemy database session.

    Returns:
        dict: Dictionary with message and list of class data, or an error.
    """
    try:
        class_name = class_name.lower()
        classes = FitnessClass.get_by_name(session, class_name)

        if not classes:
            return {'error': f'No upcoming classes found for {class_name}'}

        classes_dict = [item.to_dict() for item in classes]

        return {
            'message': f'Here is the list of upcoming {class_name} classes!',
            'data': classes_dict
        }

    except Exception as e:
        session.rollback()
        return {'error': f'Failed to retrieve classes: {str(e)}'}


@session_wrap
def create_new_fitness_class_handler(request_body: dict, session: Any) -> dict:
    """
    Creates a new fitness class after validating the request payload.

    Args:
        request_body (dict): JSON payload containing fitness class details.
        session (Any): SQLAlchemy database session.

    Returns:
        dict: Response message and data or an error dictionary.
    """
    try:
        # Validate incoming data
        is_valid = validate_fitness_class_payload(request_body)
        if 'error' in is_valid:
            return is_valid

        # Extract required fields
        name = request_body.get('name', '').lower()
        capacity = request_body.get('capacity')
        instructor = request_body.get('instructor')
        duration = request_body.get('duration')
        datetime_str = request_body.get('datetime_str')

        # Resolve class description
        description = FitnessClassDescriptionMapper.get(name)

        # Create and save the new class
        new_class = FitnessClass.create_class(
            name, datetime_str, duration, instructor, capacity, description
        )

        session.add(new_class)
        session.commit()

        return {
            'message': 'New class created successfully',
            'data': new_class.to_dict()
        }

    except Exception as e:
        session.rollback()
        return {'error': f'Failed to create class: {str(e)}'}


@session_wrap
def get_class_bookings_per_user_handler(token: str, session: Any) -> dict:
    """
    Retrieves all class bookings made by a specific user.

    Args:
        token (str): Contains ID of the user.
        session (Any): SQLAlchemy database session.

    Returns:
        dict: A dictionary containing the user's booking information or an error message.
    """
    try:
        user_id = Users.get_user_id(session, token)
        classes = Bookings.get_active_bookings(session=session, client_id=user_id)

        if not classes:
            return {'message': 'No bookings found for this user', 'data': []}

        bookings_dict = [item.to_dict() for item in classes]

        return {
            'message': 'Here is the list of your classes!',
            'data': bookings_dict
        }

    except Exception as e:
        session.rollback()
        return {'error': f'Failed to fetch bookings: {str(e)}'}


@session_wrap
def create_class_booking_per_user_handler(token: str, class_id: int, session: Any) -> dict:
    """
    Creates a booking for a user in a specified fitness class if not a booking present.

    Args:
        token (str): Contains ID of the user.
        class_id (int): The ID of the fitness class to book.
        session (Any): SQLAlchemy database session.

    Returns:
        dict: A response containing the booking information or an error message.
    """

    try:
        user_id = Users.get_user_id(session, token)

        # Check for existing booking
        existing_booking = Bookings.get_existing_booking(session, class_id, user_id)
        if existing_booking:
            return {
                'message': 'You already have a booking for the same class',
                'data': existing_booking.to_dict()
            }

        fitness_class = FitnessClass.get_by_id(session, class_id, True, True)

        if not fitness_class:
            return {'error': 'Class not found or is not eligible for booking'}

        if fitness_class.available_slots < 1:
            return {'error': 'No slots available for this class.'}

        # Decrease slot and create booking
        fitness_class.available_slots -= 1

        booking = Bookings.create_booking(class_id=class_id, client_id=user_id)
        booking.status = BookingStatus.CONFIRMED.value

        session.add(fitness_class)
        session.add(booking)
        session.commit()

        return {
            'message': 'Booking successful!',
            'data': booking.to_dict()
        }

    except Exception as e:
        session.rollback()
        return {'error': f'Error booking class: {str(e)}'}


@session_wrap
def cancel_user_class_booking_handler(token: str, booking_id: int, session: Any) -> dict:
    """
    Cancels a booking for a user.

    Args:
        token (str): Contains ID of the user.
        booking_id (int): The ID of the booking to cancel.
        session (Any): SQLAlchemy database session.

    Returns:
        dict: A response containing the booking information or an error message.
    """
    try:
        user_id = Users.get_user_id(session, token)

        booking = Bookings.get_by_id(session, booking_id)
        if booking.status == BookingStatus.CANCELLED.value:
            return {'error': 'Booking is already cancelled'}

        # validates booking is of the logged-in user only
        if booking.client_id != user_id:
            return {'error': 'You are not allowed to cancel this booking'}

        booking.status = BookingStatus.CANCELLED.value

        class_id = booking.class_id
        fitness_class = FitnessClass.get_by_id(session, class_id, True, True)

        # Free up the slot
        fitness_class.available_slots += 1

        session.add(fitness_class)
        session.add(booking)
        session.commit()

        return {
            'message': 'Booking cancelled!',
            'data': booking.to_dict()
        }

    except Exception as e:
        session.rollback()
        return {'error': f'Error cancelling booking: {str(e)}'}
