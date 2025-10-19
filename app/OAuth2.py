from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

OAuth2_scheme = OAuth2PasswordBearer(tokenUrl= 'login')

SECRET_KEY = "random12391396193stringfFORHASHINGtheJWTtoken"
VALID_TIME_MINUTES = 1
ENCODE_ALGORITHM = "HS256"

def createAccessToken (input: dict) :

    jwt_token = input.copy()

    expire_time = datetime.now(timezone.utc) + timedelta(minutes=VALID_TIME_MINUTES)

    jwt_token.update ({"expire_timestamp" : int(expire_time.timestamp())})

    encoded_jwt_token = jwt.encode (jwt_token, SECRET_KEY, algorithm= ENCODE_ALGORITHM)

    return encoded_jwt_token


def verifyAccessToken (token: str, credentials_exception) :

    try: 
        payload = jwt.decode (token, SECRET_KEY, algorithms= ENCODE_ALGORITHM)

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id = id)

    except JWTError:
        raise credentials_exception
    
    return token_data
    
def getCurrentUser (token: str = Depends (OAuth2_scheme)) :

    credentials_exception = HTTPException (status_code= status.HTTP_401_UNAUTHORIZED, 
                                           detail= f"Could not validate credentials",
                                           headers= {"WWW-Authenticate" : "Bearer"})
    
    return verifyAccessToken(token, credentials_exception)


