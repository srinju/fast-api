from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel) :
    title : str
    body : str
    

class User(BaseModel) :
    name : str
    email : str
    password : str


class showUser(User) :
    name:str
    email : str
    blogs : list[Blog]

    class Config() :
        orm_mode = True


#schema for the blog we will show the user
class showBlog(Blog) : 
    title:str
    body:str
    creator:showUser
    
    class Config() :
        orm_mode = True


class Login(BaseModel) :
    email : str
    password : str
    

class Token(BaseModel) :
    access_token : str
    token_type : str


class TokenData(BaseModel) :    
    email : Optional[str] = None