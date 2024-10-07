from fastapi import FastAPI, Depends, HTTPException, status , Form
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import List

import uvicorn
import json

from auth import get_password_hash, create_access_token, get_current_user, verify_password
from authModels import Token, UserCreate, TokenData
from dbModels import User, Base, get_db, Project, Task

import sys
import os

# Ajouter le chemin parent au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#importer les fonctions du fichier main.py
from llm.main import generate_tasks_API, convert_to_json
from llm.llmModels import responseModel

app = FastAPI()

# racine de l'API
@app.get("/")
def read_root():
    return {"Hello": "World"}

#--- Routes pour l'authentification ---
# Endpoint pour l'inscription d'un nouvel utilisateur
@app.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Créer un nouvel utilisateur
    new_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Créer un token d'accès pour l'utilisateur
    access_token = create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint pour la connexion d'un utilisateur
@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur existe
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # Créer un token d'accès pour l'utilisateur
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

#---------------------------------------


#--- Routes pour les tâches ---

# Endpoint pour génerer une liste de tâches
@app.post("/generate_tasks")
def generate_tasks(userMessage: str = Form(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not userMessage:
        raise HTTPException(status_code=400, detail="User message is required")

    # Faire un appel à la fonction get_all_tasks() du fichier main.py
    apiResponse = generate_tasks_API(userMessage)
    
    # Convertir la réponse en JSON
    responseJSON = convert_to_json(apiResponse)
    
    # Extraire le projet et les tâches de la réponse
    data = json.loads(responseJSON)
    if 'project' not in data or 'tasks' not in data:
        raise HTTPException(status_code=400, detail="Invalid response format")
    
    project = data['project']
    tasks = data['tasks']

    # Insérer le projet dans la base de données
    new_project = Project(name=project, user_id=current_user.id)
    db.add(new_project)
    db.commit()

    # Récupérer l'ID du projet nouvellement inséré
    project_id = new_project.id

    # Insérer les tâches dans la base de données
    for task in tasks:
        new_task = Task(title=task['title'], done=task['done'], project_id=project_id, user_id=current_user.id)
        db.add(new_task)
    
    # Commit les ajouts en une seule fois
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Task generation failed: {str(e)}")

    return {"detail": "Task generation successful"}

@app.get("/projects")
def get_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Récupérer les projets associés à l'utilisateur connecté
    projects = db.query(Project).filter(Project.user_id == current_user.id).all()
    
    if not projects:
        raise HTTPException(status_code=404, detail="No projects found for the current user")
    
    return projects




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")