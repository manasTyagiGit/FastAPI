from fastapi import Depends, HTTPException, FastAPI, status, Response
from .database import engine, get_db
from typing import List
from . import models, schemas
from sqlalchemy.orm import Session
from . import utils

app = FastAPI()



#To create all models via the engine in database.py
models.Base.metadata.create_all(bind=engine)

# R - read all posts
@app.get ("/posts", status_code= status.HTTP_200_OK, response_model= List[schemas.PostResponse])
def getAllPosts(conn: Session = Depends(get_db)) :
    posts = conn.query(models.Post).all()
    return posts

# R - read a post by id
@app.get("/posts/{id}", status_code= status.HTTP_200_OK, response_model= schemas.PostResponse)
def getPostById (id: int, conn : Session = Depends(get_db)) :
    post = conn.query(models.Post).filter(models.Post.id == id)

    if not post.first() :
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                             detail= f"Post with id = {id} not found")
    
    return post.first()


# C - Create a new post
@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def createPost (post: schemas.PostCreate, conn : Session = Depends(get_db)) :
    new_post_obj = models.Post(**post.model_dump())        # unpacking a dict
        

    conn.add(new_post_obj)
    conn.commit()
    conn.refresh(new_post_obj)

    return new_post_obj
    
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
@app.put ("/posts/{id}", status_code= status.HTTP_200_OK, response_model= schemas.PostResponse)
def updatePostById (id: int, post: schemas.PostUpdate, conn : Session = Depends(get_db)) :
    updPost = conn.query(models.Post).filter(models.Post.id == id)

    if updPost.first() is None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} was not found, 404"
        )
    
    updPost.update(post.model_dump(), synchronize_session = False)
    conn.commit()

    return updPost.first()   


@app.post("/users", status_code= status.HTTP_201_CREATED, response_model = schemas.UserResponse)
def create_user(user: schemas.UserCreate, conn: Session = Depends(get_db)) :

    password_hash = utils.hash(user.password)

    user.password = password_hash

    new_user = models.User(**user.model_dump())

    conn.add(new_user)
    conn.commit()
    conn.refresh(new_user)

    return new_user

