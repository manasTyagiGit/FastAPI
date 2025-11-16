from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# For protecting routes by making FastAPI expect token in Authorization header, 
# and telling FastAPI -> User to use login/ to get token
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl= 'login')

SECRET_KEY = "random12391396193stringfFORHASHINGtheJWTtoken"
VALID_TIME_MINUTES = 60
ENCODE_ALGORITHM = "HS256"

def createAccessToken (input: dict) :

    jwt_token = input.copy()

    expire_time = datetime.now(timezone.utc) + timedelta(minutes=VALID_TIME_MINUTES)

    # use 'exp' only, as it is checked automatically by jwt.decode during verification
    jwt_token.update ({"exp" : int(expire_time.timestamp())})               
    encoded_jwt_token = jwt.encode (jwt_token, SECRET_KEY, algorithm= ENCODE_ALGORITHM)

    return encoded_jwt_token


def verifyAccessToken (token: str, credentials_exception) :

    try: 
        payload = jwt.decode (token, SECRET_KEY, algorithms= ENCODE_ALGORITHM)

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        # Converting to Pydantic schema type/instance
        token_data = schemas.TokenData(user_id = id)

    except JWTError:
        raise credentials_exception
    
    return token_data
    
def getCurrentUser (token: str = Depends(OAuth2_scheme), conn: Session = Depends(database.get_db)) :

    credentials_exception = HTTPException (status_code= status.HTTP_401_UNAUTHORIZED, 
                                           detail= f"Could not validate credentials",
                                           headers= {"WWW-Authenticate" : "Bearer"})
    
    ret_token = verifyAccessToken (token, credentials_exception)

    user = conn.query(models.User).filter(models.User.id == ret_token.user_id).first()
    
    return user

