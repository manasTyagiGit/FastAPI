from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body

# for schema validation
from pydantic import BaseModel

app = FastAPI()

# class for extension of BaseModel
class Body (BaseModel) :
    title: str
    content: str
    #Defaultable optional
    published: bool = True
    #Truly Optional
    rating: Optional[int] = None


@app.get("/")
def first_api() :
    return {"Hello" : "Welcome to my first api!"}

@app.get("/getposts")
def get_posts() :
    return {"Hey user_name" : "These are your posts"}

@app.post("/createposts")
def create_posts(post_body : Body) :
    print (post_body)
    print (post_body.model_dump())
    return {"post_data" : post_body}