from fastapi import Depends, HTTPException, status, APIRouter
from .. import schemas, utils, models

from ..database import get_db
from sqlalchemy.orm import Session

# Setting router
router = APIRouter(
    prefix= "/users",
    tags = ['Users']
)


# C- Create a new user, append it to the DB table
@router.post("/", status_code= status.HTTP_201_CREATED, response_model = schemas.UserResponse)
def create_user(user: schemas.UserCreate, conn: Session = Depends(get_db)) :

    password_hash = utils.hash(user.password)

    user.password = password_hash

    # Unpack the dict to match model fields
    new_user = models.User(**user.model_dump())

    conn.add(new_user)
    conn.commit()
    conn.refresh(new_user)

    return new_user

# R - Read a user using id, this has multiple uses, including authentication
@router.get("/{id}", response_model = schemas.UserResponse)
def get_user_by_id (id: int, conn = Depends(get_db)) :
    user = conn.query(models.User).filter(models.User.id == id).first()

    if not user :
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                             detail= f"User with id: {id} not found")
    
    return user