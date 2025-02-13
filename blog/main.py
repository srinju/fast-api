from fastapi import FastAPI
from . import  models 
from .database import engine
from .routers import blog
from .routers import user

app = FastAPI();

#create the table in the db>

models.Base.metadata.create_all(engine)

app.include_router(blog.router)

app.include_router(user.router)