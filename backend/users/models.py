from datetime import datetime, timedelta
from pytz import timezone
from sqlalchemy import (
    func, Column, String, Integer, DateTime, Boolean, ForeignKey, JSON, Time, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError
from sql_config import Base
from extensions import bcrypt


class Users(Base):

    __tablename__ = "Users"

    prim_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True, default=None)
    mobile = Column(Integer, unique=True, nullable=True, default=None)
    password = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False)
    is_admin = Column(Boolean, default=False)
    dt_created = Column(DateTime, default=func.now())
    dt_updated = Column(DateTime, onupdate=func.now(), default=func.now())

    def __init__(self, name, email, mobile, password, is_admin=False):
        self.name = name
        self.email = email
        self.mobile = mobile
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        self.is_admin = is_admin

    @classmethod
    def get_by_id(cls, session, user_id: int):
        return session.query(cls).filter_by(prim_id=user_id).first()

    @classmethod
    def get_by_ids(cls, session, user_ids: list):
        return session.query(cls).filter(cls.prim_id.in_(user_ids)).all()

    @classmethod
    def get_by_email(cls, session, email: str):
        return session.query(cls).filter_by(email=email).first()

    @classmethod
    def get_by_mobile(cls, session, mobile: str):
        return session.query(cls).filter_by(mobile=mobile).first()

    def to_dict(self):
        return {
            'prim_id': self.prim_id,
            'name': self.name,
            'email': self.email,
            'mobile': self.mobile,
            'is_admin': self.is_admin,
        }

    def __repr__(self):
        return f"<User {self.name}>"
