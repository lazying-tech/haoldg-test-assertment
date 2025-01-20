from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.book_model import Book
from models.author_model import Author
from utils.validation_schemas import BookCreate,BookUpdate
from sqlalchemy.exc import IntegrityError

def create_book(db: Session, book: BookCreate):
    # Check for duplicate ISBN
    db_book = db.query(Book).filter(Book.isbn == book.isbn).first()
    db_author=db.query(Author).filter(Author.id==book.author_id).first()
    if db_book:
        raise HTTPException(status_code=400, detail="ISBN already exists")
    
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    new_book = Book(**book.model_dump())
    db.add(new_book)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Database constraint error: ISBN must be unique")
    db.refresh(new_book)
    return new_book
def update_book(
    db: Session,
    book_id: int,
    book_update: BookUpdate  # Expecting structured input
):
    # Retrieve the book and author
    db_book = db.query(Book).filter(Book.id == book_id).first()
    db_author = (
        db.query(Author).filter(Author.id == book_update.author_id).first()
        if book_update.author_id is not None
        else None
    )

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book_update.author_id is not None and not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    # Update fields only if provided; otherwise, retain current values
    for key, value in book_update.dict(exclude_unset=True).items():
        if hasattr(db_book, key):
            setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)

    # Convert the SQLAlchemy model to a dictionary for raw response
    return {
        "id": db_book.id,
        "title": db_book.title,
        "author_id": db_book.author_id,
        "published_date": db_book.published_date.isoformat() if db_book.published_date else None,
        "isbn": db_book.isbn,
        "price": db_book.price,
    }

def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def list_books(db: Session, fields: list = None):
    query = db.query(Book)
    
    query.all()
    result = []
    for book in query:
        book_dict = {}
        if "id" in fields:
            book_dict["id"] = book.id
        if "title" in fields:
            book_dict["title"] = book.title
        if "author_id" in fields:
            book_dict["author_id"] = book.author_id
        if "published_date" in fields:
            book_dict["published_date"] = book.published_date
        if "price" in fields:
            book_dict["price"] = book.price
        result.append(book_dict)

    return result

def delete_book(db: Session, book_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book

