from fastapi import FastAPI,Body,Path,Query,HTTPException
from pydantic import BaseModel,Field
from typing import Optional
from starlette import status

app = FastAPI()

class book:
    id:int
    title:str
    author:str
    description:str
    rating:int
    publish_date:int

    def __init__(self,id,title,author,description,rating,publish_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating 
        self.publish_date=publish_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title:str = Field(min_length=3)
    author:str = Field(min_length=1)
    description:str = Field(min_length=1, max_length=100)
    rating:int = Field(gt=0,lt=6)
    publish_date:int = Field(gt=2000,lt=3000)

    model_config={
        "json_schema_extra":{
            "example":{
                "title":"A New Book",
                "author" : "Author Six",
                "description" : "A good Book",
                "rating" : 4,
                "publish_date": 2012
            }
        }
    }

BOOKS=[
    book(1,"Computer","author one","a very nice book",4.8,2012),
    book(2,"English","author two","a very nice book",4.4,2001),
    book(3,"Science","author two","a average book",3.5,2003),
    book(4,"History","author four","a nice book",3.8,2022),
    book(5,"English","author one","a very nice book",4.2,2021)
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/book/", status_code=status.HTTP_200_OK)
async def book_by_publish_date(pusbish:int = Query(gt=2000,lt=3001)):
    books_to_return = []
    for book in BOOKS:
        if book.publish_date == pusbish:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def book_by_ID(book_id:int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_books_by_rating(book_rating : int = Query(gt=0,lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return        

@app.post("/create_books", status_code=status.HTTP_201_CREATED)
async def create_book(book_req:BookRequest):
    new_book = book(**book_req.model_dump())
    BOOKS.append(find_id(new_book))

def find_id(book:book):
    if len(BOOKS)>0:
        book.id = BOOKS[-1].id +1
    else:
        book.id=1

    return book 

@app.put("/books/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(books: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == books.id:
            BOOKS[i]=book(**books.model_dump())
            book_changed=True
    if not book_changed:
        raise HTTPException(status_code=404,detail="Item not Found")

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int =Path(gt=0)):
    book_chg = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_chg = True
            break
    if not book_chg:
        raise HTTPException(status_code=404,detail="Item not Found")    
