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
from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
app = FastAPI(title="This is my model")
class task(BaseModel):
    id:int
    title:str
    description:str
    completed:bool

tasks_db={
    "1":{"id":"1","title":"Hells","description":"lkdjdklsajd"}
}
@app.get("/health",response)
def health():
    return {"Status":"Healthy"}
@app.get("/task/{task_id}",response)
def task_get(task_id:int):
    if task_id in tasks_db:
        return tasks_db.get(task_id)
@app.post("/item")
async def postitem(item:task):
    tasks_db.append(item.model_dump())
    return tasks_db
@app.patch("/item/{item_id}")
async def itempatch(item_id:int,item:task):
    if item_id not in tasks_db:
        return None
    return item
@app.delete("/item/{item_id}")
async def itemdelete(item_id:int,item):
    if item_id in tasks_db:
        del tasks_db[item_id]
        return True


