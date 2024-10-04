from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


# Modèles pour la réponse de l'API
class responseModel(BaseModel):

    class TaskModel(BaseModel):
        title: str
        done: bool 

    project: str
    task: list[TaskModel]
# ----------------------------

# Modèles pour la base de données

  