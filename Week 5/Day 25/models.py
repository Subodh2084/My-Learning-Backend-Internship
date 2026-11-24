"""
Day 25 Database Models
SQLAlchemy models matching the Shared Contract: User and Task entities.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()


class PriorityEnum(str, enum.Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"


class TaskStatusEnum(str, enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    token = Column(String(120), unique=True, nullable=False)

    # Relationships
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(80), nullable=False)
    priority = Column(SQLEnum(PriorityEnum), default=PriorityEnum.NORMAL, nullable=False)
    status = Column(SQLEnum(TaskStatusEnum), default=TaskStatusEnum.OPEN, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Relationship back to User
    owner = relationship("User", back_populates="tasks")
