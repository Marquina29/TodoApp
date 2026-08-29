from database import Base
from sqlalchemy import Column,INTEGER,String,Boolean,ForeignKey

class Users(Base):
    __tablename__= 'users'

    id = Column(INTEGER,primary_key=True,index=True)
    mail = Column(String,unique=True)
    username = Column(String,unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active= Column(String,default=True)
    role = Column(String)

class Todos(Base):
    __tablename__ = 'todos'

    id= Column(INTEGER,primary_key=True,index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(INTEGER)
    complete = Column(Boolean,default=False)
    owner = Column(INTEGER, ForeignKey("users.id"))