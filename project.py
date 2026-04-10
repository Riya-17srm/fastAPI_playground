from fastapi import FastAPI, Depends
from database import get_db, engine
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import date
import model
from fastapi.exceptions import HTTPException, status

app=FastAPI()

class BookStore(BaseModel):
    id: int
    title: str
    author: str
    publish_date: date 


@app.post("/book")
def create_book(book: BookStore, db: Session= Depends(get_db)):
    new_book= model.Book(id=book.id, title=book.title, author=book.author, publish_date= book.publish_date)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/books")
def get_book(db: Session=Depends(get_db)):
    books=db.query(model.Book).all()
    return books

@app.delete("/books/{book_id}")
def remove_book(book_id:int, db: Session=Depends(get_db)):
    book=db.query(model.Book).filter(model.Book.id==book_id).first()
    
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")   
    db.delete(book)
    db.commit()
    return {"Message": f"Book {book_id} Removed" }
    
         