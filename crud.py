from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.exceptions import HTTPException

books = [
    {
        "id": 1,
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "publish_date": "1988-01-01"
    },
    {
        "id": 2,
        "title": "The God of Small Things",
        "author": "Arundhati Roy",
        "publish_date": "1997-04-04"
    },
    {
        "id": 3,
        "title": "The White Tiger",
        "author": "Aravind Adiga",
        "publish_date": "2008-01-01"
    },
    {
        "id": 4,
        "title": "The Palace of Illusions",
        "author": "Chitra Banerjee Divakaruni",
        "publish_date": "2008-02-12"
    }
]

app=FastAPI()

@app.get("/book")
def get_book():
    return books


@app.get("/")
def read_root():
    return {"Message": "Hello World"}

class Book(BaseModel):
    id:int
    title:str
    author:str
    publish_date:str

@app.post("/create_book")
def create_book(book: Book):
    new_book=book.model_dump()
    books.append(new_book)
    return {"message": "Book added", "book": new_book}

@app.get("/book/{book_id}")
def get_book(book_id:int):
    for book in books:
        if(book_id==book["id"]):
            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")
    
class BookUpdate(BaseModel):
    title:str
    author:str
    publish_date:str

@app.put("/book/{book_id}")
def book_update(book_id:int, book_update: BookUpdate):
    for book in books:
        if(book_id==book['id']):
            book['title']=book_update.title
            book['author']=book_update.author
            book['publish_date']=book_update.publish_date
            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")



@app.delete("/book/{book_id}")
def delete_book(book_id:int):
    for book in books:
        if(book_id==book['id']):
            books.remove(book)
            return {"Message": f"Book {book_id} Deleted",
                    "deleted_book": book
                    }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")            