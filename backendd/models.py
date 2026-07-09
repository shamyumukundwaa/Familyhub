from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    points = Column(Integer, default=0)

    chores = relationship("Chore", back_populates="assigned_user")
    requests = relationship("PermissionRequest", back_populates="child")
    events = relationship("Event", back_populates="creator")


class Chore(Base):
    __tablename__ = "chores"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    due_time = Column(String, nullable=True)
    status = Column(String, default="pending")
    requires_photo = Column(Boolean, default=False)
    points_value = Column(Integer, default=10)
    assigned_to = Column(Integer, ForeignKey("users.id"))

    assigned_user = relationship("User", back_populates="chores")


class PermissionRequest(Base):

    __tablename__ = "permission_requests"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    child_id = Column(Integer, ForeignKey("users.id"))

    child = relationship("User", back_populates="requests")


class Reward(Base):

    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    points_requires = Column(Integer, nullable=False)


class Event(Base):

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    date = Column(String, nullable=False)  # Matches your calendar.py logic
    time = Column(String, nullable=True)
    visible_to = Column(String, default="all")

    created_by = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="events")
