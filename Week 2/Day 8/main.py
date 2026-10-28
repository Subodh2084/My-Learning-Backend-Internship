from fastapi import FastAPI, HTTPException, status
from service import task_service, TaskCreate, TaskUpdate, TaskModel, TaskNotFoundError

app = FastAPI() #main app

@app.post("/tasks", response_model=TaskModel, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    return task_service.create_task(payload)

@app.get("/tasks/{task_id}", response_model=TaskModel, status_code=status.HTTP_200_OK)
def read_task(task_id: str):
    try:
        return task_service.get_task(task_id)
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Resource 'Task' with identity {task_id} does not exist."
        )

@app.patch("/tasks/{task_id}", response_model=TaskModel, status_code=status.HTTP_200_OK)
def update_task(task_id: str, payload: TaskUpdate):
    try:
        return task_service.update_task(task_id, payload)
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Cannot update. Resource 'Task' with identity {task_id} not found."
        )

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    try:
        task_service.delete_task(task_id)
        return None  
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Cannot delete. Resource 'Task' with identity {task_id} not found."
        )