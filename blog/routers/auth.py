from fastapi import APIRouter ,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas , models ,hashing , token
# from ..schemas import Token 
# from ..hashing import Hash
from ..database import get_db 
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import JWTError,jwt

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login' ,status_code = 200 ,  response_model = schemas.Token)
def login(request : OAuth2PasswordRequestForm = Depends() , db : Session = Depends(get_db)) : #get the request from oauth2passwordrequest form not from ur own schema as the fastapi wouldnt recognise it that's why
    #get the user from the email
    #then check the 
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user :
        raise HTTPException(ststus_code = 404 , detail = 'user not found please create ur account!!')
    
    if not hashing.Hash.verify(request.password , user.password ) :
        #pass is not verified -> false user
        raise HTTPException(status_code=401,detail='invalid password')
    
    #generate jwt token and return it 

    #access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = token.create_access_token(data={"sub": user.email})

    return schemas.Token(access_token=access_token, token_type="bearer")
