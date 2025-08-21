from random import randrange
from fastapi import FastAPI, Body, status, HTTPException, Response
from fastapi.params import Body


app = FastAPI()

post_store = [{"title" : "post1_title", "content" : "post1_content", "id" : 1},
              {"title" : "post2_title", "content" : "post2_content", "id" : 2}
              ]

# SAMPLE API 
@app.get("/")
def first_api() :
    return {"Status:" : "Landing page, please go to endpoint /posts for useable stuff"}


# API to get all posts
@app.get("/posts", status_code= status.HTTP_200_OK)                              # this can work only with some sort of storage
def get_posts() :
    return {"All posts:" : post_store}

# Helper function for the get_post_by_id() function
def find_by_id(id: int):
    for post in post_store :
        if post["id"] == id :
            return post
    
    return None

# API to get a post via {id} path param
@app.get("/posts/{id}", status_code= status.HTTP_200_OK)
def get_post_by_id(id: int):
    post = find_by_id (id)

    if not post :
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                             detail= f"post with id : {id} not found")
    
    return {"post found" : post}

# API to add a post 
@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_post (post: dict = Body(...)) :
    if "id" not in post:
        post["id"] = randrange(0, 1000000)

    post_store.append(post)
    return {"Created" : post}

# Helper function to return iterator to the post Dict
def find_iterator_by_id(id: int) :
    for i, p in enumerate (post_store) :
        if p["id"] == id :
            return i
    
    return None

# API to update a post using PUT
@app.put("/posts/{id}", status_code= status.HTTP_200_OK)
def update_post(id: int, post: dict = Body(...)) :
    post_iter = find_iterator_by_id(id)

    if post_iter is None :      # do not use <if not post_iter> as idx can be 0
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                             detail= f"post with id: {id} not found")
    
    post ["id"] = id
    post_store[post_iter] = post

    return {"data": post_store[post_iter]}

# API to detele a post using {id} and DELETE
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int) :
    post_iter = find_iterator_by_id (id)

    if post_iter is None :
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                             detail= f"post with id: {id} not found")

    post_store.pop(post_iter)

    return Response (status_code= status.HTTP_204_NO_CONTENT)
     