import uuid
from typing import Optional
from pydantic import BaseModel, Field

class TaskModel(BaseModel):
    id: str
    title: str
    description: str
    completed: bool = False

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskNotFoundError(Exception):
    pass

class TaskService:
    def __init__(self):
        self._storage = {}

    def create_task(self, task_data: TaskCreate) -> TaskModel:
        task_id = str(uuid.uuid4())
        new_task = TaskModel(
            id=task_id,
            title=task_data.title,
            description=task_data.description
        )
        self._storage[task_id] = new_task
        return new_task

    def get_task(self, task_id: str) -> TaskModel:
        if task_id not in self._storage:
            raise TaskNotFoundError()
        return self._storage[task_id]

    def update_task(self, task_id: str, update_data: TaskUpdate) -> TaskModel:
        if task_id not in self._storage:
            raise TaskNotFoundError()
        
        current_task = self._storage[task_id]
        updated_dict = current_task.model_dump()
        
        # Apply incoming modifications selectively
        for key, value in update_data.model_dump(exclude_unset=True).items():
            updated_dict[key] = value
            
        updated_task = TaskModel(**updated_dict)
        self._storage[task_id] = updated_task
        return updated_task

    def delete_task(self, task_id: str) -> None:
        if task_id not in self._storage:
            raise TaskNotFoundError()
        del self._storage[task_id]

# Global Singleton Service Instantiation
task_service = TaskService()
