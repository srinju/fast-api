from fastapi import APIRouter
from fastapi import FastAPI,Depends,status,Response , HTTPException #type:ignore
from .. import schemas , models , hashing
from ..database import engine,get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/blog",
    tags=['blogs']
);

@router.get('/' , status_code=200 , response_model = list[schemas.showBlog], tags=['blogs'])
def getBlogs(db : Session = Depends(get_db)) :
    blogs = db.query(models.Blog).all() #query from the db with the model.blog meaning the model we want and .all is all of it
    if not blogs :
        raise HTTPException(status_code = 404 , detail = 'blogs were not there!!')
    
    return blogs


@router.post('/' , status_code=status.HTTP_201_CREATED )
def createBlog(request : schemas.Blog , db : Session = Depends(get_db)) :
    
    new_blog = models.Blog(title=request.title , body=request.body , user_id = 1) #defingin the bolg model that is going to be input in the db
    db.add(new_blog) #add the new blog in the db
    db.commit() # commit it
    db.refresh(new_blog) #refresh it
    return new_blog


@router.get('/{id}' , status_code = 200 , response_model = schemas.showBlog ) #response model is schema.blog that means it will not show id
def getSingleBlog(id , response : Response , db : Session = Depends(get_db)) :
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog :
        raise HTTPException(status_code=404 , detail = f'blog with the {id} was not found')
    
        '''
        response.status_code = 404
        return {'error' : f'blog with the {id} was not found'}
        '''
    return blog


@router.delete('/{id}' , status_code=204 )
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


@router.put('/{id}', status_code = 202 )
def updateBlog(id ,request : schemas.Blog , db : Session = Depends(get_db)) : #we need the req body to update the blog
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first() :
        raise HTTPException(status_code = 404 , detail=f'blog with {id} was not found!!')
    
    blog.update(request.dict())
    db.commit()
    return f'the blog with id {id} was updated successfully!! '
