from fastapi import FastAPI
import uvicorn
from config.db import init_db,insert_demo_data
from endpoints import author_endpoint, book_endpoint



# Initialize FastAPI
# Initialize database
app = FastAPI()

init_db()
insert_demo_data()
@app.get("/")
async def index():
    return {"message": "Hello World"}
# Include routers
app.include_router(book_endpoint.book_router, prefix="/books", tags=["books"])
app.include_router(author_endpoint.author_router, prefix="/authors", tags=["authors"])

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8008, reload=True)