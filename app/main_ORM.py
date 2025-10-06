from fastapi import Depends, HTTPException, FastAPI, status, Response
from .database import engine, get_db
from typing import Optional
from . import models
from sqlalchemy.orm import Session
from pydantic import BaseModel

app = FastAPI()

#To create all models via the engine in database.py
models.Base.metadata.create_all(bind=engine)

class PostBody (BaseModel) :
    id: Optional[int] = None
    title: str
    content: str
    #Defaultable optional
    published: bool = True
    #Truly Optional
    #rating: Optional[int] = None

# R - read all posts
@app.get ("/posts", status_code= status.HTTP_200_OK)
def getAllPosts(conn: Session = Depends(get_db)) :
    posts = conn.query(models.Post).all()
    return {"posts" : posts}

# R - read a post by id
@app.get("/posts/{id}", status_code= status.HTTP_200_OK)
def getPostById (id: int, conn : Session = Depends(get_db)) :
    post = conn.query(models.Post).filter(models.Post.id == id)

    if not post.first() :
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                             detail= f"Post with id = {id} not found")
    
    return {"Post found" : post.first()}


# C - Create a new post
@app.post("/posts", status_code = status.HTTP_201_CREATED)
def createPost (post: PostBody, conn : Session = Depends(get_db)) :

    existing_post = conn.query(models.Post).filter(models.Post.id == post.id)

    if existing_post.first() :
        updated_post = updatePostById (post.id, post, conn)
        return {"updated existing post" : updated_post}

    new_post_obj = models.Post(**post.model_dump())        # unpacking a dict
        

    conn.add(new_post_obj)
    conn.commit()
    conn.refresh(new_post_obj)

    return {"new post" : new_post_obj}
    
# D - delete a post by id
@app.delete ("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def deletePostById (id: int, conn : Session = Depends(get_db)) :
    delPost = conn.query(models.Post).filter(models.Post.id == id)

    if delPost.first() is None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} was not found, 404"
        )
    
    delPost.delete(synchronize_session = False)
    conn.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)

# U - Update post by id
@app.put ("/posts/{id}", status_code= status.HTTP_200_OK)
def updatePostById (id: int, post:PostBody, conn : Session = Depends(get_db)) :
    updPost = conn.query(models.Post).filter(models.Post.id == id)

    if updPost.first() is None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} was not found, 404"
        )
    
    updPost.update(post.model_dump(), synchronize_session = False)
    conn.commit()

    return {"updated post" : updPost.first()}
    

