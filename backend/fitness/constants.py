from enum import Enum


class BookingStatus(Enum):
    INIT = 'init'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
