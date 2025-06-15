from enum import Enum


class FitnessClasses(Enum):
    ZUMBA = 'zumba'
    YOGA = 'yoga'
    HIIT = 'hiit'


class BookingStatus(Enum):
    INIT = 'init'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'


Fitness_Class_Description_Mapper = {
    FitnessClasses.ZUMBA.value: "Low-weight dance",
    FitnessClasses.YOGA.value: "Evening relaxation",
    FitnessClasses.HIIT.value: "High intensity interval training"
}

MaxClassDuration = 90  # in minutes
MaxClassCapacity = 50
