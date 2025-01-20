from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base



class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    published_date = Column(Date, nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    price = Column(Float, nullable=False)
    author = relationship("Author", back_populates="books")