"""
Day 25 Database Engine and Seeder
Initializes database session and seeds multi-user synthetic dataset.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, User, Task, PriorityEnum, TaskStatusEnum

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> Session:
    """Sets up schema and initial seed users and tasks."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    # User 1: Alice
    alice = User(id=1, email="alice@taskflow.dev", token="token-alice-secret")
    # User 2: Bob
    bob = User(id=2, email="bob@taskflow.dev", token="token-bob-secret")
    session.add_all([alice, bob])
    session.commit()

    # Seed initial tasks
    t1 = Task(id=1, title="Review Ariadne GraphQL schema", priority=PriorityEnum.HIGH, status=TaskStatusEnum.IN_PROGRESS, owner_id=1)
    t2 = Task(id=2, title="Document REST vs GraphQL parity", priority=PriorityEnum.NORMAL, status=TaskStatusEnum.OPEN, owner_id=1)
    t3 = Task(id=3, title="Bob's private analysis task", priority=PriorityEnum.LOW, status=TaskStatusEnum.OPEN, owner_id=2)
    session.add_all([t1, t2, t3])
    session.commit()

    return session
