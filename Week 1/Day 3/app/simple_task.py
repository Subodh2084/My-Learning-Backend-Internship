from .task_service import validate_title,validate_priority
from typing import Dict,Any
#simple create task function that takes input as dict and output dict
def create_task(task_data:dict[str,Any],next_id:int)->Dict[str,Any]:
    title=task_data.get("title","")
    priority=task_data.get("priority",3)
    validate_title(title)
    validate_priority(priority)
    return {
        "title":title,
        "priority":priority,
        "next_id":next_id
    }
    