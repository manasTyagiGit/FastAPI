from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post, user, auth, like

# Importing Cross Origin Resource Sharing = CORS
from fastapi.middleware.cors import CORSMiddleware

# app is an object of FastAPI that handles all operations
app = FastAPI()

# Setting up CORS, Middleware runs before every functions
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# To create all models via the engine in database.py
models.Base.metadata.create_all(bind=engine)

# including functionality via router files
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)