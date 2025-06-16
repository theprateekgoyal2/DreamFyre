import logging
from datetime import datetime
from .constants import FitnessClasses, MaxClassDuration, MaxClassCapacity


def validate_fitness_class_payload(payload: dict) -> dict:
    """
    Validates the payload for creating a new fitness class.

    Args:
        payload (dict): The input data containing class details.

    Returns:
        dict: A dictionary containing 'message': 'success' if valid, or 'error': <message> if invalid.
    """
    try:
        # Validate class name
        name = payload.get('name')
        if not name or name.lower() not in [
            FitnessClasses.ZUMBA.value,
            FitnessClasses.YOGA.value,
            FitnessClasses.HIIT.value,
        ]:
            return {'error': 'Invalid or missing class name'}

        # Validate instructor name
        instructor = payload.get('instructor')
        if not instructor or not isinstance(instructor, str) or not instructor.strip():
            return {'error': 'Instructor name must be a non-empty string'}

        # Validate duration
        duration = payload.get('duration')
        if not isinstance(duration, int) or duration <= 0 or duration > MaxClassDuration:
            return {'error': f'Duration must be an integer between 1 and {MaxClassDuration}'}

        # Validate capacity
        capacity = payload.get('capacity')
        if not isinstance(capacity, int) or capacity <= 0 or capacity > MaxClassCapacity:
            return {'error': f'Capacity must be an integer between 1 and {MaxClassCapacity}'}

        # Validate datetime string
        datetime_str = payload.get('datetime_str')
        if not datetime_str:
            return {'error': 'Missing datetime string'}

        datetime_obj = datetime.fromisoformat(datetime_str)  # This will raise ValueError if invalid

        return {'message': 'success'}

    except Exception as e:
        logging.info(f'Validation error: {str(e)}')
        return {'error': f'Invalid payload: {str(e)}'}
