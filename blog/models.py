from .database import Base
from sqlalchemy import Column,Integer,String ,ForeignKey
from sqlalchemy.orm import relationship

#define the model of the blog for the db
class Blog(Base) :
    __tablename__ = 'blogs'

    id = Column(Integer , primary_key=True , index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User" , back_populates="blogs")

#model for user for the db >>

class User(Base) :
    __tablename__ = 'users'

    id = Column(Integer , primary_key=True , index = True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship("Blog" , back_populates="creator")