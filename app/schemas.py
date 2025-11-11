from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# class for extension of BaseModel
class PostCreate (BaseModel) :
    title: str
    content: str
    #Defaultable optional
    published: bool = True
    #Truly Optional
    #rating: Optional[int] = None

class PostUpdate (PostCreate) :
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class PostResponse (PostCreate) :
    id: int
    created_at: datetime
    # The below is used to make sure Pydantic can interact
    # with the returned Class objects by ORM logic, as 
    # Pydantic generally interacts with dict objects
    class Config:
        orm_mode = True 

class UserCreate (BaseModel) :
    email: EmailStr
    password: str

class UserResponse (BaseModel) :
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin (BaseModel) :
    email: EmailStr
    password: str

class TokenInput (BaseModel) :
    access_token: str
    type: str

class TokenData (BaseModel):
    user_id : Optional[int] = None
