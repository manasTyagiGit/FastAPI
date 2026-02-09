from fastapi import Depends, HTTPException, status, Response, APIRouter
from .. import schemas, utils, models, OAuth2

from ..database import get_db
from sqlalchemy.orm import Session

# Setting router
router = APIRouter(
    prefix= "/likes",
    tags = ['Likes']
)


@router.post("/", status_code = status.HTTP_201_CREATED)
def likePost(like: schemas.Like, conn: Session = Depends(get_db), current_user: models.User = Depends(OAuth2.getCurrentUser)) :

    post_query = conn.query(models.Post).filter(models.Post.id == like.post_id)
    post_found = post_query.first()

    if not post_found :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {like.post_id} does not exist")

    like_query = conn.query(models.Like).filter(models.Like.post_id == like.post_id, models.Like.user_id == current_user.id)

    like_found = like_query.first()

    if like.dir == 1 :
        if like_found :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Post with id = {like.post_id} already liked by user with id = {current_user.id}")
        
        new_like = models.Like(post_id = like.post_id, user_id = current_user.id)
        conn.add(new_like)
        conn.commit()

        return {"message" : "You liked the post"}

    else :
        if not like_found :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post with id = {like.post_id} already un-liked by user with id = {current_user.id}")
        
        like_query.delete(synchronize_session=False)
        conn.commit()

        return {"message" : "You un-liked the post"}

