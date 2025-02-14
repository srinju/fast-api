from fastapi import APIRouter
from fastapi import FastAPI,Depends,status,Response , HTTPException 
from .. import schemas , models , hashing
from ..database import engine,get_db
from sqlalchemy.orm import Session
    

router = APIRouter(
    prefix="/user",
    tags=['users']
);

#create user>>

@router.post('/' , status_code = 201, response_model = schemas.showUser)
def createUser(request : schemas.User , db : Session = Depends(get_db)) :
    hashedPassword = hashing.Hash.bcrypt(request.password) # hash the password

    #check for existing users with that email >>
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if user :
        raise HTTPException(status_code = 409 , detail=f'user with email {request.email} already exists ')

    newUser = models.User(name=request.name , email=request.email , password = hashedPassword)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser

#get user by id >>
@router.get('/{id}',status_code = 200 , response_model = schemas.showUser)
def getUser(id,db : Session = Depends(get_db)) :
    #get the user with that id
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user :
        raise HTTPException(status_code = 404 , detail='user not found')
    
    return user
