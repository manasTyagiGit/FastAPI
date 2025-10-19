from fastapi import Depends, HTTPException, status, Response, APIRouter
from typing import List
from .. import schemas, utils, models, OAuth2

from ..database import get_db
from sqlalchemy.orm import Session


# Setting router
router = APIRouter(
    prefix= "/posts",
    tags = ['Posts']
)

# R - read all posts
@router.get ("/", status_code= status.HTTP_200_OK, response_model= List[schemas.PostResponse])
def getAllPosts(conn: Session = Depends(get_db)) :
    posts = conn.query(models.Post).all()
    return posts

# R - read a post by id
@router.get("/{id}", status_code= status.HTTP_200_OK, response_model= schemas.PostResponse)
def getPostById (id: int, conn : Session = Depends(get_db)) :
    post = conn.query(models.Post).filter(models.Post.id == id)

    if not post.first() :
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                             detail= f"Post with id = {id} not found")
    
    return post.first()


# C - Create a new post
@router.post("/", status_code = status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def createPost (post: schemas.PostCreate, conn : Session = Depends(get_db), current_user: int  = Depends(OAuth2.getCurrentUser)) :
    new_post_obj = models.Post(**post.model_dump())        # unpacking a dict
        

    conn.add(new_post_obj)
    conn.commit()
    conn.refresh(new_post_obj)

    return new_post_obj
    
# D - delete a post by id
@router.delete ("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def deletePostById (id: int, conn : Session = Depends(get_db), current_user: int  = Depends(OAuth2.getCurrentUser)) :
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
@router.put ("/{id}", status_code= status.HTTP_200_OK, response_model= schemas.PostResponse)
def updatePostById (id: int, post: schemas.PostUpdate, conn : Session = Depends(get_db), current_user: int  = Depends(OAuth2.getCurrentUser)) :
    updPost = conn.query(models.Post).filter(models.Post.id == id)

    if updPost.first() is None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} was not found, 404"
        )
    
    updPost.update(post.model_dump(), synchronize_session = False)
    conn.commit()

    return updPost.first()   