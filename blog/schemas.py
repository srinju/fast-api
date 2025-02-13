from pydantic import BaseModel #type:ignore

class Blog(BaseModel) :
    title : str
    body : str


#schema for the blog we will show the user
class showBlog(Blog) : 
    class Config() :
        orm_mode = True


class User(BaseModel) :
    name : str
    email : str
    password : str


class showUser(User) :
    name:str
    email : str
    class Config() :
        orm_mode = True