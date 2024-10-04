from fastapi import FastAPI
import uvicorn

import models
import bdd
from main import generate_task_API

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

#endpoint to generate tasks 
@app.get("/generate_tasks/{userInput}")
def generate_tasks(userInput: str):
    result = generate_task_API(userInput)
    return result

#endpoint to get all tasks
@app.get("/tasks")
def get_all_tasks():
    tasks = bdd.get_all_tasks()
    return tasks