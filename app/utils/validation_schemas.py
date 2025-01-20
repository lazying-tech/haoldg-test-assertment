from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class AuthorBase(BaseModel):
    name: str
    nationality: Optional[str]

class AuthorCreate(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    id: int
    class Config:
        from_attributes = True

class BookBase(BaseModel):
    title: str
    author_id: int
    published_date: date
    isbn: str
    price: float = Field(gt=0, description="Price must be positive")

class BookCreate(BookBase):
    pass
class BookUpdate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    author: Optional[AuthorResponse]
    class Config:
        from_attributes = True
