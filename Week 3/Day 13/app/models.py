from sqlalchemy import Column, Integer, String, Boolean,Float
from app.database import Base

# --- SQLAlchemy Model ---
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)
    salary = Column(Float)

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', completed={self.is_completed})>"


# --- Repository Functions ---
def create_task(session, title: str, description: str = None) -> Task:
    """Inserts a new task stage into the session tracking state."""
    new_task = Task(title=title, description=description)
    session.add(new_task)
    # Flush pushes changes to the DB transaction without committing the outer scope
    session.flush() 
    return new_task

def get_all_tasks(session):
    """Retrieves all tasks present in the current committed database snapshot."""
    return session.query(Task).all()

def get_task_by_id(session, task_id: int) -> Task:
    """Retrieves a single task by ID."""
    return session.query(Task).filter(Task.id == task_id).first()
