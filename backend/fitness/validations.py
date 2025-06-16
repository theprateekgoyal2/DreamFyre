from datetime import datetime
from .constants import FitnessClasses, MaxClassDuration, MaxClassCapacity


def validate_fitness_class_payload(payload: dict) -> dict:
    name = payload.get('name')
    if not name or name.lower() not in [
        FitnessClasses.ZUMBA.value,
        FitnessClasses.YOGA.value,
        FitnessClasses.HIIT.value,
    ]:
        return {'error': 'Invalid or missing class name'}

    instructor = payload.get('instructor')
    if not instructor or not isinstance(instructor, str) or not instructor.strip():
        return {'error': 'Instructor name must be a non-empty string'}

    duration = payload.get('duration')
    if not duration or not isinstance(duration, int) or int(duration) <= 0 or int(duration) > MaxClassDuration:
        return {'error': f'Duration must be a between 0 to {MaxClassDuration}'}

    try:
        capacity = int(payload.get('capacity'))
        datetime_str = payload.get('datetime_str')
        if capacity <= 0 or capacity > MaxClassCapacity:
            return {'error': f'Capacity must be between 0 to {MaxClassCapacity}'}

        datetime_obj = datetime.fromisoformat(datetime_str)

    except Exception as e:
        return {'error': f'{str(e)}'}

    return {'message': 'success'}
