

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils.validation_schemas import AuthorCreate,AuthorResponse
from services import author_service 
from config.db import get_db

author_router = APIRouter()

@author_router.post("/", response_model=AuthorResponse)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return author_service.create_author(db=db, author=author)




@author_router.delete("/{author_id}", response_model=dict)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = author_service.delete_author(db=db, author_id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="author not found")
    return {"message": "author deleted successfully"}
