import random
from datetime import datetime, timedelta
from sql_config import session_wrap
from fitness.models import FitnessClass, Bookings
from fitness.constants import FitnessClasses, BookingStatus, FitnessClassDescriptionMapper
from users.models import Users

# Sample names
NAMES = ["prateek", "ananya", "rajat", "megha", "aditya", "neha", "siddharth", "isha", "arjun", "priya"]
INSTRUCTORS = ["Ravi Kumar", "Anjali Mehta", "Nitin Sharma"]
CLASSES = [FitnessClasses.ZUMBA.value, FitnessClasses.YOGA.value, FitnessClasses.HIIT.value]


def populate_users(session, count: int = 10):
    """
    Populates the Users table with dummy data. Each user will have either an email or a mobile, not both.
    Also stores the plain text password for reference (e.g., during login tests).
    """
    users = []
    base_mobile = 9000000000

    for i in range(count):
        name = NAMES[i % len(NAMES)]
        plain_password = "WarrenBuffet"

        # Decide randomly whether to assign an email or a mobile
        use_email = random.choice([True, False])
        email = f"{name.lower()}_test{i}@yopmail.com" if use_email else None
        mobile = None if use_email else base_mobile + i

        user = Users(
            name=name.capitalize(),
            email=email,
            mobile=mobile,
            password=plain_password
        )

        session.add(user)
        users.append((user, plain_password))

    session.commit()
    return users


def populate_fitness_classes(session, count_per_type: int = 3):
    fitness_classes = []
    for class_name in CLASSES:
        for i in range(count_per_type):
            class_datetime = str(datetime.now() + timedelta(days=i, hours=random.randint(1, 6)))
            duration = random.randint(30, 90)
            capacity = random.randint(10, 45)
            instructor = random.choice(INSTRUCTORS)

            fitness_class = FitnessClass.create_class(
                name=class_name,
                description=FitnessClassDescriptionMapper[class_name],
                datetime_str=class_datetime,
                duration_minutes=duration,
                instructor=instructor,
                capacity=capacity,
            )
            session.add(fitness_class)
            fitness_classes.append(fitness_class)
    session.commit()
    return fitness_classes


def populate_bookings(session, users, classes):
    booked = set()
    for user_obj, _ in users:
        for fitness_class in random.sample(classes, k=min(2, len(classes))):
            key = (user_obj.prim_id, fitness_class.prim_id)
            if key in booked:
                continue

            if fitness_class.available_slots <= 0:
                continue

            booking = Bookings(
                class_id=fitness_class.prim_id,
                client_id=user_obj.prim_id,
                status=BookingStatus.CONFIRMED.value,
                booked_at=datetime.utcnow()
            )
            session.add(booking)
            fitness_class.available_slots -= 1
            booked.add(key)
    session.commit()


@session_wrap
def run_all_populations(session):
    users = populate_users(session)
    classes = populate_fitness_classes(session)
    populate_bookings(session, users, classes)
    print("Database population complete.")
    print("Users and their plaintext passwords:")
    for user_obj, plain_pwd in users:
        print(f"{user_obj.name} - {user_obj.email if user_obj.email else user_obj.mobile} - {plain_pwd}")


if __name__ == '__main__':
    run_all_populations()

