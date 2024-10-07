from pydantic import BaseModel


# Modèles pour la réponse de l'API
class responseModel(BaseModel):

    class TaskModel(BaseModel):
        title: str
        done: bool 

    project: str
    task: list[TaskModel]
# ----------------------------