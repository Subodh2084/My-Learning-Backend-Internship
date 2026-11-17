from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Optional

app = FastAPI()

# --- Models & Mock Database ---
class Task(BaseModel):
    id: str
    owner: str
    title: str
    content: str

# Mock database partitioned by task ID
db: Dict[str, Task] = {
    "task_alice_1": Task(id="task_alice_1", owner="alice", title="Alice's Secret", content="Top secret data"),
    "task_bob_1": Task(id="task_bob_1", owner="bob", title="Bob's Task", content="Bob's public draft")
}

# --- Authentication Mock ---
# Separates identification (who you are) from authorization (what you can do)
def get_current_user(username: str) -> dict:
    if username not in ["alice", "bob", "admin_user"]:
        raise HTTPException(status_code=401, detail="Could not authenticate user")
    
    role = "admin" if username == "admin_user" else "user"
    return {"username": username, "role": role}

# --- Shared Service Logic (Enforcing Task Ownership) ---
def verify_ownership_or_admin(task_id: str, current_user: dict) -> Task:
    if task_id not in db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = db[task_id]
    
    # Core Concept: Authenticated identity != Permission to act
    if current_user["role"] != "admin" and task.owner != current_user["username"]:
        raise HTTPException(
            status_code=403, 
            detail="Permission denied: You do not own this resource"
        )
    return task

# --- API Endpoints ---

@app.get("/tasks/{task_id}")
def read_task(task_id: str, user: dict = Depends(get_current_user)):
    task = verify_ownership_or_admin(task_id, user)
    return task

@app.put("/tasks/{task_id}")
def edit_task(task_id: str, updated_title: str, user: dict = Depends(get_current_user)):
    task = verify_ownership_or_admin(task_id, user)
    task.title = updated_title
    return {"message": "Task updated successfully", "task": task}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str, user: dict = Depends(get_current_user)):
    task = verify_ownership_or_admin(task_id, user)
    del db[task_id]
    return {"message": f"Task {task_id} deleted successfully"}

# --- Explicit Administrator-Only Action ---
@app.post("/admin/purge-system-logs")
def purge_system_logs(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Permission denied: Restricted to administrators only"
        )
    return {"status": "success", "message": "System logs permanently purged."}
