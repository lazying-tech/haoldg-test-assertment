from fastapi import  Depends, HTTPException
from sqlalchemy.orm import Session
from models.author_model import Author
from utils.validation_schemas import AuthorCreate
from config.db import get_db

def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    new_author = Author(**author.model_dump())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(db_author)
    db.commit()
    return {"message": "Author deleted successfully"}