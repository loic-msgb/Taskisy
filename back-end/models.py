from pydantic import BaseModel



class responseModel(BaseModel):

    class Task(BaseModel):
        title: str
        done: bool 
        
    project: str
    task: list[Task]