from sqlalchemy import create_engine,text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import session,sessionmaker
from ..database import Base
from ..main import app
from..routers.todos import get_db,current_user
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from ..models import Todos

SQLALCHAMY_DATABASE_URL= 'sqlite:///./testdb.db'

engine = create_engine(SQLALCHAMY_DATABASE_URL,connect_args={"check_same_thread":False},poolclass=StaticPool,)

TestingSessionLoacal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base.metadata.create_all(bind=engine)

def overried_get_db():
    db = TestingSessionLoacal()
    try:
        yield db
    finally:
        db.close()

def overried_get_current_user():
    return {'username':'admin2','id':1,'user_role':'admin'}

app.dependency_overrides[get_db] = overried_get_db
app.dependency_overrides[current_user] = overried_get_current_user

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo=Todos(
        title="Learn to code!!",
        description="Learn everyday",
        priority =5,
        complete = False,
        owner=1
    )

    db=TestingSessionLoacal()
    db.add(todo)
    db.commit()
    yield db
    with engine.connect() as connection:
        connection.execute(text("Delete from todos;"))
        connection.commit()

def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()==[{'complete':False,'title':'Learn to code!!','description':'Learn everyday','id':1,'priority':5,
                            'owner':1
                            }]


