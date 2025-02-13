from fastapi import FastAPI,Depends,status,Response , HTTPException #type:ignore
from . import schemas , models , hashing
from .database import engine,SessionLocal
from sqlalchemy.orm import Session


app = FastAPI();

#create the table in the db>

models.Base.metadata.create_all(engine)

def get_db() :
    db = SessionLocal()
    try : 
        yield db    
    finally :
        db.close()


@app.post('/blog' , status_code=status.HTTP_201_CREATED , tags=['blogs'])
def createBlog(request : schemas.Blog , db : Session = Depends(get_db)) :
    
    new_blog = models.Blog(title=request.title , body=request.body , user_id = 1) #defingin the bolg model that is going to be input in the db
    db.add(new_blog) #add the new blog in the db
    db.commit() # commit it
    db.refresh(new_blog) #refresh it
    return new_blog

#get the blogs from the db>>

@app.get('/blog' , status_code=200 , response_model = list[schemas.showBlog], tags=['blogs'])
def getBlogs(db : Session = Depends(get_db)) :
    blogs = db.query(models.Blog).all() #query from the db with the model.blog meaning the model we want and .all is all of it
    if not blogs :
        raise HTTPException(status_code = 404 , detail = 'blogs were not there!!')
    
    return blogs

@app.get('/blog/{id}' , status_code = 200 , response_model = schemas.showBlog , tags=['blogs']) #response model is schema.blog that means it will not show id
def getSingleBlog(id , response : Response , db : Session = Depends(get_db)) :
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog :
        raise HTTPException(status_code=404 , detail = f'blog with the {id} was not found')
    
        '''
        response.status_code = 404
        return {'error' : f'blog with the {id} was not found'}
        '''
    return blog


@app.delete('/blog/{id}' , status_code=204 , tags=['blogs'])
def deleteBlog(id,db : Session = Depends(get_db)) :
    #deelte blog >>
    #get the blog with that id>
    blogWithId = db.query(models.Blog).filter(models.Blog.id == id)

    if not blogWithId.first() :
        raise HTTPException(status_code=404 , detail=f'the blog with the id {id} was not found!')
    
    #blog found>>
    #delete the blog>
    blogWithId.delete(synchronize_session=False)
    db.commit()

    return {
        f'blog with {id} was deleted!!!'
    }


@app.put('/blog/{id}', status_code = 202 , tags=['blogs'])
def updateBlog(id ,request : schemas.Blog , db : Session = Depends(get_db)) : #we need the req body to update the blog
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first() :
        raise HTTPException(status_code = 404 , detail=f'blog with {id} was not found!!')
    
    blog.update(request.dict())
    db.commit()
    return f'the blog with id {id} was updated successfully!! '


#create user>>

@app.post('/user' , status_code = 201, response_model = schemas.showUser , tags=['users'])
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
@app.get('/user/{id}',status_code = 200 , response_model = schemas.showUser , tags=['users'])
def getUser(id,db : Session = Depends(get_db)) :
    #get the user with that id
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user :
        raise HTTPException(status_code = 404 , detail='user not found')
    
    return user
