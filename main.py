from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from random import randrange

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

#Storing posts here, i.e., a list of dictionaries
all_posts = [{"title": "title of post 1", "content": "content of post 1", "id" : 1},
             {"title": "title of post 2", "content": "content of post 2", "id" : 2}
            ]


@app.get("/")
def first_api() :
    return {"Hello" : "Welcome to my first api!"}

@app.get("/posts")
def get_posts() :
    return {"Hey user, posts are" : all_posts}

@app.post("/posts")
def create_posts(post : Body) :

    post_dict = post.model_dump()
    
    post_dict['id'] = randrange (0, 10000000)

    all_posts.append(post_dict)

    return {"post_data" : post_dict}

def find_by_id (id: int) :
    for post in all_posts :
        if post["id"] == id :
            return post
    
    return None

@app.get("/posts/{id}")         # 'id' is a path parameter
def get_post_by_id (id: int) :
    post = find_by_id (id)

    if post != None:
        return {"detail" : post}

    return {"detail": f"post with id : {id} not found"}