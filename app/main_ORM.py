from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post, user, auth

# app is an object of FastAPI that handles all operations
app = FastAPI()

# To create all models via the engine in database.py
models.Base.metadata.create_all(bind=engine)

# including functionality via router files
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)