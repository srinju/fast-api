from fastapi import FastAPI # type: ignore
from pydantic import BaseModel # type: ignore
#from pydantic import Optional # type: ignore

app = FastAPI() #instance of the fastapi

@app.get('/blog') #path operarion decorator
def index(limit=10,published : bool=True , sort=True) : #path operaation function
    #in the url it will be in form of >> http://127.0.0.1:8000/blog?limit=10&published=true
    if published == True:
        return { 'data' : f'blog list of {limit} from the db'}
    
    return { 'data' : 'no published blogs'}


class Blog(BaseModel) :
    title : str
    body : str
    #published_at : Optional[bool]


@app.post('/blog')
def createBlog(request : Blog) :

    return {
        'data' : f'blog is created with {request.title} and {request.body}'
    }

#whenever creating dynamic routing remb to put them at the last

@app.get('/blog/unpublished')
def unpublished() :
    return  {
        'data' : 'all unpublished blogs'
    }


@app.get('/blog/{id}')
def show(id : int) :
    return {
        'data' : id
    }


@app.get('/blog/{id}/comments')
def blogComments(id,limit=10) : 
    return {
        'data' : {
            f'comments of {id} blog' : f'{limit} comments' 
        }
    
    }


