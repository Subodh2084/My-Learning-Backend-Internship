"""
Day 24 Database Engine & Synthetic Data Seeder
Provides request-scoped sessions and pre-populates users, projects, and tasks for testing pagination and N+1 queries.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, User, Project, Task, TaskStatus

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> Session:
    """Creates database schema and seeds synthetic multi-user dataset."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # User 1: Alice (owns 30 tasks across 2 projects)
    alice = User(id=1, username="alice", email="alice@example.com", token="alice-secret-token")
    # User 2: Bob (owns 10 tasks in 1 project)
    bob = User(id=2, username="bob", email="bob@example.com", token="bob-secret-token")
    db.add_all([alice, bob])
    db.commit()

    proj_a1 = Project(id=1, name="Alice Core Infrastructure", owner_id=1)
    proj_a2 = Project(id=2, name="Alice GraphQL Gateway", owner_id=1)
    proj_b1 = Project(id=3, name="Bob Analytics Lab", owner_id=2)
    db.add_all([proj_a1, proj_a2, proj_b1])
    db.commit()

    # Seed 30 tasks for Alice (to test pagination boundaries)
    alice_tasks = []
    for i in range(1, 31):
        status = TaskStatus.DONE if i % 3 == 0 else (TaskStatus.IN_PROGRESS if i % 2 == 0 else TaskStatus.OPEN)
        proj_id = 1 if i <= 15 else 2
        alice_tasks.append(
            Task(id=i, title=f"Alice Task #{i:02d}", status=status, owner_id=1, project_id=proj_id)
        )
    db.add_all(alice_tasks)

    # Seed 10 tasks for Bob
    bob_tasks = []
    for i in range(31, 41):
        bob_tasks.append(
            Task(id=i, title=f"Bob Task #{i:02d}", status=TaskStatus.OPEN, owner_id=2, project_id=3)
        )
    db.add_all(bob_tasks)

    db.commit()
    return db
