from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 


#in this file we specify thr databse url
# create the engine
#do all the session locker shit 

SQLALCHAMY_DATABASE_URL = 'sqlite:///./blog.db'


engine = create_engine(SQLALCHAMY_DATABASE_URL , connect_args={"check_same_thread":False})

#create session >

SessionLocal = sessionmaker(bind=engine , autocommit = False , autoflush=False,)

#mappping >>

Base = declarative_base()

def get_db() :
    db = SessionLocal()
    try : 
        yield db    
    finally :
        db.close()

