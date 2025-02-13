from pydantic import BaseModel #type:ignore

class Blog(BaseModel) :
    title : str
    body : str
