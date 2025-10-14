from fastapi import Depends, HTTPException, FastAPI, status, Response
from .database import engine, get_db
from typing import List
from . import models, schemas
from sqlalchemy.orm import Session
from . import utils
from .routers import post, user


app = FastAPI()

#To create all models via the engine in database.py
models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(user.router)