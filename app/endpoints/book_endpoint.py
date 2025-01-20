from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils.validation_schemas import BookCreate,BookResponse,BookUpdate
from services import book_service 
from config.db import get_db

book_router = APIRouter()

@book_router.post("/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return book_service.create_book(db=db, book=book)


@book_router.patch("/{book_id}")
def update_book(book_id: int,book_update: BookUpdate, db: Session = Depends(get_db)):
    return book_service.update_book(db=db, book_id=book_id,book_update=book_update)

@book_router.get("/{book_id}", response_model=BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = book_service.get_book(db=db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@book_router.get("/", response_model=list)
def list_books(
    author_id: Optional[bool] = None,
    published_date: Optional[bool] = None,
    title: Optional[bool] = None,
    price: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    fields = [
        field
        for field, include in {
            "author_id": author_id,
            "published_date": published_date,
            "title": title,
            "price": price,
        }.items()
        if include  # Include only fields that are True
    ]
    return book_service.list_books(db=db, fields=fields)

@book_router.delete("/{book_id}", response_model=dict)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = book_service.delete_book(db=db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
