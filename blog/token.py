from datetime import datetime, timedelta, timezone
from jose import JWTError,jwt

SECRET_KEY = "secret"

ALGORITHM = "HS256"

ACESS_TOKEN_EXPIRE_MINUTES = 200

# function to create access token>>

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt