from fastapi import APIRouter, Response, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas
from .. import models
from .. import utils


router = APIRouter(
    prefix= "/login",
    tags = ['Authentication']
)

@router.post("/")
def user_login (user_cred: schemas.UserLogin, conn: Session = Depends(get_db)) :

    # check is user mail exists in the stored DB table for users
    user = conn.query(models.User).filter (models.User.email == user_cred.email).first()

    if not user :
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                             detail = f"Email ID does not match")
    
    # Email exists, but check password given, and already stored password    
    if not utils.verify(user_cred.password, user.password) :
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                             detail = f"Password does not match")
    
    # create JWT Token

    # return JWT Token

    return {"JWT Token" : "Sample token"}
    
     


