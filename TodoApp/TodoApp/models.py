from database import Base
from sqlalchemy import Column,INTEGER,String,Boolean

class Todos(Base):
    __tablename__ = 'todos'

    id= Column(INTEGER,primary_key=True,index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(INTEGER)
    complete = Column(Boolean,default=False)