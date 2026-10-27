from fastapi import FastAPI,status

from pydantic import BaseModel,Field,ConfigDict
from typing import Optional
from typing import Optional
class TaskCreateInput(BaseModel):                   #this is validation for task input
    name:str=Field(...,min_length=5,max_length=50)
    description:Optional[str]=None
    model_config=ConfigDict(extra="ignore")
class TaskResponse(BaseModel):                      #this is check for task output
    id:int
    name:str
    description:Optional[str]=None

app= FastAPI()

@app.post("/task",response_model=TaskResponse,status_code=status.HTTP_201_CREATED,summary="This is post router")
async def create_task(task:TaskCreateInput):
    answer={
        "id":1,
        "name":task.name,
        "description":task.description      
    }
    return answer 
if __name__=="__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="localhost", port=5000, reload=True)
