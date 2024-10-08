# fichier pour les fonctions qui gèrent les tâches

from sqlalchemy.orm import Session
from fastapi import HTTPException
from dbModels import User, Base, get_db, Project, Task

#fonction pour avoir l'id d'un projet
def get_project_id(project_name: str, db: Session):
    project = db.query(Project).filter(Project.name == project_name).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project.id

#fonction pour avoir les tâches d'un projet
def get_project_tasks(project_id: int, db: Session):
    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    return tasks

#fonction pour choisir les tâches à afficher
def get_tasks_to_display(tasks, done: bool, num_tasks: int):
    filtered_tasks = [task for task in tasks if task.done == done]
    return filtered_tasks[:num_tasks]