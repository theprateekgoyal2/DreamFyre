from datetime import datetime, timedelta
from pytz import timezone
from sqlalchemy import (
    func, Column, String, Integer, DateTime, Boolean, ForeignKey, JSON, Time, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError
from sql_config import Base
from .constants import BookingStatus

IST = timezone("Asia/Kolkata")


class FitnessClass(Base):
    __tablename__ = 'FitnessClass'

    prim_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    datetime = Column(DateTime(timezone=True), nullable=False)
    duration = Column(Integer, nullable=False)
    instructor = Column(String(100), nullable=False)
    available_slots = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    is_cancelled = Column(Boolean, default=False)
    dt_created = Column(DateTime, default=func.now())
    dt_updated = Column(DateTime, onupdate=func.now(), default=func.now())

    def __repr__(self):
        return f"<FitnessClass id={self.prim_id} name='{self.name}' at {self.datetime}>"

    @classmethod
    def create_class(
            cls,
            name: str,
            datetime_str: str,
            duration_minutes: int,
            instructor: str,
            capacity: int,
            description: str = None
    ):
        try:
            # Incoming datetime is naive (no tz info), but you assume it's IST*
            naive_dt = datetime.fromisoformat(datetime_str)
            class_datetime = IST.localize(naive_dt)

        except ValueError:
            raise ValueError("Invalid datetime format. Use ISO format (e.g., '2025-06-15T08:00:00').")

        return cls(
            name=name,
            description=description,
            datetime=class_datetime,
            duration=duration_minutes,
            instructor=instructor,
            available_slots=capacity,
            capacity=capacity,
        )

    @classmethod
    def get_by_id(cls, session, class_id: int, with_for_update=False, no_wait=False):
        if with_for_update:
            return session.query(cls).with_for_update(nowait=no_wait).filter_by(prim_id=class_id).first()
        return session.query(cls).filter_by(prim_id=class_id).first()

    @classmethod
    def get_by_ids(cls, session, class_ids: list):
        return session.query(cls).filter(cls.prim_id.in_(class_ids)).all()

    @classmethod
    def get_by_name(cls, session, name):
        return session.query(cls).filter_by(name=name).all()

    def to_dict(self):
        return {
            'class_id': self.prim_id,
            'name': self.name,
            'description': self.description,
            'datetime': str(self.datetime),
            'duration': self.duration,
            'instructor': self.instructor,
            'available_slots': self.available_slots,
            'capacity': self.capacity,
            'is_cancelled': self.is_cancelled,
        }


class Bookings(Base):
    __tablename__ = 'Bookings'

    prim_id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('FitnessClass.prim_id'), nullable=False)
    client_id = Column(Integer, ForeignKey('Users.prim_id'), nullable=False)
    booked_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default=BookingStatus.INIT.value)
    dt_created = Column(DateTime, default=func.now())
    dt_updated = Column(DateTime, onupdate=func.now(), default=func.now())

    fitness_class = relationship("FitnessClass", backref="Bookings")
    client = relationship("Users", backref="Bookings")

    def __repr__(self):
        return f"<Booking id={self.prim_id} for class_id={self.class_id} by {self.client_id}>"

    @classmethod
    def create_booking(cls, class_id, client_id):
        return cls(
            class_id=class_id,
            client_id=client_id,
            booked_at=datetime.utcnow()
        )

    @classmethod
    def get_by_id(cls, session, booking_id):
        return session.query(cls).filter_by(prim_id=booking_id).first()

    @classmethod
    def get_by_client_id(cls, session, client_id):
        return session.query(cls).filter_by(client_id=client_id).all()

    @classmethod
    def get_existing_booking(cls, session, class_id, client_id):
        return session.query(cls).filter_by(client_id=client_id, class_id=class_id, status=BookingStatus.CONFIRMED.value).first()

    def to_dict(self):
        return {
            "booking_id": self.prim_id,
            "class_id": self.class_id,
            "client_id": self.client_id,
            "booked_at": str(self.booked_at),
            "status": self.status,
        }
