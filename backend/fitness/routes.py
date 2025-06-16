from .apis import (get_fitness_classes_api, get_class_bookings_per_user_api, create_new_fitness_class_api,
                   create_class_booking_per_user_api)

api_routes = [
    ('/api/classes', get_fitness_classes_api, ['GET']),
    # Fetch all upcoming classes

    ('/api/classes', create_new_fitness_class_api, ['POST']),
    # Admin or staff creates a new class

    ('/api/users/bookings', create_class_booking_per_user_api, ['POST']),
    # User books a class

    ('/api/users/bookings', get_class_bookings_per_user_api, ['GET'])
    # User views their own bookings
]
