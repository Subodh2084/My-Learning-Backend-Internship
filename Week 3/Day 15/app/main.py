from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
#from models import create_task, get_all_tasks

app = FastAPI()

SessionDep = Annotated[Session, Depends(get_db)]


@app.on_event("startup")
def on_startup() -> None:
  
  Base.metadata.create_all(bind=engine)
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
  

# @app.post("/tasks/")
# def add_task(title: str, session: SessionDep):
#   try:
#     task = create_task(session, title=title)
#     return {"status": "success", "task": str(task)}
#   except Exception as e:
#     raise HTTPException(status_code=400, detail=str(e))


# @app.get("/tasks/")
# def list_tasks(session: SessionDep):
#   all_tasks = get_all_tasks(session)
#   return {"tasks": all_tasks}
from models import Task,User
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import IntegrityError
import os

# ==========================================
# PYDANTIC SCHEMAS (Validation)
# ==========================================
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    user_id: int

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int

    class Config:
        from_attributes = True

# ==========================================
# ONSITE STEP 2: HEALTH CHECK & DEPENDENCY FAILURE
# ==========================================
@app.get("/health", status_code=status.HTTP_200_OK)
def health_check(db: Session = Depends(get_db)):
    try:
        # Execute a simple query to verify database connectivity
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database dependency failure: {str(e)}"
        )

# ==========================================
# CORE API ENDPOINTS (Acceptance Checks)
# ==========================================
@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    try:
        db_task = Task(title=task.title, user_id=task.user_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except IntegrityError as e:
        db.rollback()
        # Captures both Duplicate constraints and Invalid Foreign Key References
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Integrity constraint violation. Verify that user_id exists and title is valid."
        )

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()
# seed.py


# Clean slate initialization
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = get_db()
try:
    # Replay seed data
    test_user = User(username="dev_user")
    SessionDep.add(test_user)
    SessionDep.commit()
    print("Seed successful: Database recreated and base user seeded.")
finally:
    SessionDep.close()

