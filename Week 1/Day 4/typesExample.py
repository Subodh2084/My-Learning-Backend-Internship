from typing import List, Literal, TypedDict
#using type hint
class Task(TypedDict):
    id: int
    title: str
    completed: bool

class AppConfig(TypedDict):
    port: int
    environment: Literal['development', 'production', 'staging']

class TaskService:
    def __init__(self) -> None:
        self.tasks: List[Task] = []

    #Inside a function
    def create_task(self, id: int, title: str) -> Task:
        new_task: Task = {
            "id": id,
            "title": title,
            "completed": False
        }
        self.tasks.append(new_task)
        return new_task

service = TaskService()
service.create_task("People","This is title")
#This should cause type error






#this is the use of .env
import os

def load_config() -> dict:
    port_raw = os.getenv("PORT", "5000")
    
    try:
        port = int(port_raw)
    except ValueError:
        port = 3000
        
    environment = os.getenv("ENVIRONMENT", "development")
    if environment not in ['development', 'production', 'staging']:
        environment = 'development'
        
    return {
        "port": port,
        "environment": environment
    }

config = load_config()
print(f"Running on Port: {config['port']} inside [{config['environment']}] environment.")
