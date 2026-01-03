from fastapi import Depends, HTTPException, status, Response, APIRouter
from typing import List, Optional
from .. import schemas, utils, models, OAuth2
from sqlalchemy import and_

from ..database import get_db
from sqlalchemy.orm import Session

import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


# Setting router
router = APIRouter(
    prefix= "/posts",
    tags = ['Posts']
)

# R - read all posts
@router.get ("/", status_code= status.HTTP_200_OK, response_model= List[schemas.PostResponse])
def getAllPosts(conn: Session = Depends(get_db), current_user: models.User = Depends(OAuth2.getCurrentUser), limit: int = 3, skip: int = 0, search: Optional[str] = "") :

    base_query = conn.query(models.Post)
    if search :
        base_query = base_query.filter(and_(
            models.Post.owner_id == current_user.id, 
            models.Post.title.ilike(f"%{search}%")
            )
        )
    
    else :
        base_query = base_query.filter(models.Post.owner_id == current_user.id)

    posts = base_query.limit(limit).offset(skip).all()
    return posts

# R - read a post by id
@router.get("/{id}", status_code= status.HTTP_200_OK, response_model= schemas.PostResponse)
def getPostById (id: int, conn : Session = Depends(get_db), current_user: models.User = Depends(OAuth2.getCurrentUser)) :
    post_query = conn.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post :
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                             detail= f"Post with id = {id} not found")

    elif post.owner_id != current_user.id :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Post with id: {id} is not owned by you"
        )
    
    return post


# C - Create a new post
@router.post("/", status_code = status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def createPost (post: schemas.PostCreate, conn : Session = Depends(get_db), current_user: models.User = Depends(OAuth2.getCurrentUser)) :
    #LOGGER.info(f"Current User ID: {current_user.id}, Username: {current_user.email}")

    new_post_obj = models.Post(owner_id = current_user.id, **post.model_dump())        # unpacking a dict
        

    conn.add(new_post_obj)
    conn.commit()
    conn.refresh(new_post_obj)

    return new_post_obj
    
# D - delete a post by id
@router.delete ("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def deletePostById (id: int, conn : Session = Depends(get_db), current_user: int = Depends(OAuth2.getCurrentUser)) :
    delPost_query = conn.query(models.Post).filter(models.Post.id == id)

    delPost = delPost_query.first()

    if delPost is None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} was not found, 404"
        )

    elif delPost.owner_id != current_user.id :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Post with id: {id} is not owned by you"
        )

    
    delPost_query.delete(synchronize_session = False)
    conn.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)

# U - Update post by id
@router.put ("/{id}", status_code= status.HTTP_200_OK, response_model= schemas.PostResponse)
def updatePostById (id: int, post: schemas.PostUpdate, conn : Session = Depends(get_db), current_user: int = Depends(OAuth2.getCurrentUser)) :
    updPost_query = conn.query(models.Post).filter(models.Post.id == id)

    updPost = updPost_query.first()

    if updPost is None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} was not found, 404"
        )

    elif updPost.owner_id != current_user.id :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Post with id: {id} is not owned by you"
        )

    
    #updPost.update(post.model_dump(), synchronize_session = False)
    updPost_query.update(post.model_dump(exclude_unset=True), synchronize_session=False)

    conn.commit()

    return updPost   