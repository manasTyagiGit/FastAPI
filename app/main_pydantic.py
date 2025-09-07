from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


# Class for Pydantic model which guides the post API body
class Post (BaseModel) :
    title: str
    content: str
    name: str = "Requestor"                 # defaulted optional
    published_at: Optional[int] = None      # truly optional


app = FastAPI()

@app.get("/")
def base_func() :
    return {"status" : "success"}