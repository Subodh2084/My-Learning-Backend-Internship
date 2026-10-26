from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool


tasks_db = [
    {
        "id": 1,
        "title": "Learn FastAPI Lifecycle",
        "description": "Master ASGI, Uvicorn, Routing, and Pydantic validation.",
        "completed": True,
    }
]

# 1. Health Route
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 2. Task List Route
@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks_db

# 3. Create Task Route
@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    tasks_db.append(task.model_dump())
    return task

# Run the app 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
