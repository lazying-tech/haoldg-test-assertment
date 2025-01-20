from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base





DATABASE_URL = "mysql+pymysql://admin:admin@127.0.0.1:3306/bookstore"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from models.author_model import Author
from models.book_model import Book

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def insert_demo_data():
    db = SessionLocal()
    try:
        # Check if data already exists
        if not db.query(Author).first():
            # Insert demo authors if not exists
            if not db.query(Author).filter(Author.name == "Author One").first():
                author1 = Author(name="Author One", nationality="USA")
                db.add(author1)
            if not db.query(Author).filter(Author.name == "Author Two").first():
                author2 = Author(name="Author Two", nationality="UK")
                db.add(author2)
            db.commit()

            # Fetch inserted authors
            author1 = db.query(Author).filter(Author.name == "Author One").first()
            author2 = db.query(Author).filter(Author.name == "Author Two").first()

            # Insert demo books if not exists
            if not db.query(Book).filter(Book.isbn == "1234567890123").first():
                book1 = Book(
                    title="Book One",
                    author_id=author1.id,
                    published_date="2023-01-01",
                    isbn="1234567890123",
                    price=19.99
                )
                db.add(book1)
            if not db.query(Book).filter(Book.isbn == "9876543210987").first():
                book2 = Book(
                    title="Book Two",
                    author_id=author2.id,
                    published_date="2023-06-01",
                    isbn="9876543210987",
                    price=29.99
                )
                db.add(book2)
            db.commit()
    finally:
        db.close()
