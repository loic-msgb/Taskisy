from fastapi import FastAPI
import uvicorn

import models


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
