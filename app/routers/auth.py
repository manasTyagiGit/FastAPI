from fastapi import APIRouter, Response, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..database import get_db
from .. import schemas
from .. import models
from .. import utils
from .. import OAuth2


router = APIRouter(
    prefix= "/login",
    tags = ['Authentication']
)

@router.post("/", status_code = status.HTTP_202_ACCEPTED, response_model = schemas.TokenInput)
def user_login (user_cred: OAuth2PasswordRequestForm = Depends(), conn: Session = Depends(get_db)) :

    # check is user mail exists in the stored DB table for users
    # in ouath2, username, and password are the only two fields
    user = conn.query(models.User).filter (models.User.email == user_cred.username).first()

    if not user :
        raise HTTPException (status_code= status.HTTP_403_FORBIDDEN,
                             detail = f"Email ID does not match")
    
    # Email exists, but check password given, and already stored password    
    if not utils.verify(user_cred.password, user.password) :
        raise HTTPException (status_code= status.HTTP_403_FORBIDDEN,
                             detail = f"Password does not match")
    
    # create JWT Token
    access_token = OAuth2.createAccessToken (input = {"user_id": user.id})

    # return JWT Token
    return {"access_token" : access_token,
            "type" : "Bearer"}
