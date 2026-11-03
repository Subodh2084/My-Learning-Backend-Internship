from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, get_db_session
from models import create_task, get_all_tasks

app = FastAPI()

SessionDep = Annotated[Session, Depends(get_db_session)]


@app.on_event("startup")
def on_startup() -> None:
  Base.metadata.create_all(bind=engine)


@app.post("/tasks/")
def add_task(title: str, session: SessionDep):
  try:
    task = create_task(session, title=title)
    return {"status": "success", "task": str(task)}
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))


@app.get("/tasks/")
def list_tasks(session: SessionDep):
  all_tasks = get_all_tasks(session)
  return {"tasks": all_tasks}
