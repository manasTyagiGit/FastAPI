from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey

class Post(Base) :
    __tablename__ = "posts"

    id         =     Column (Integer, primary_key = True, nullable = False)
    title      =     Column (String, nullable = False)
    content    =     Column (String, nullable = False)
    published  =     Column (Boolean, server_default = 'TRUE', nullable = False)
    created_at =     Column (TIMESTAMP(timezone=True), nullable = False,
                             server_default=func.now())
    owner_id   =     Column (Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
class User(Base):

    __tablename__ = "users"

    email       =   Column (String, nullable = False, unique = True)
    password    =   Column (String, nullable = False)
    id          =   Column (Integer, primary_key = True, nullable = False)
    created_at  =   Column(TIMESTAMP(timezone=True), nullable=False,
                            server_default=func.now()
)

