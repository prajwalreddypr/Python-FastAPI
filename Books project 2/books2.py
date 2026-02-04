from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    
    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        
class BookRequest(BaseModel):
    id: Optional[int] = Field(description = "ID is not needed on create", default = None)
    title: str = Field(min_length = 3)
    author: str = Field(min_length = 1)
    description: str = Field(min_length = 1, max_length = 10000)
    rating: int = Field(gt=0, lt=5)
    
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "New Book",
                "author": "Prajwal Reddy",
                "description": "History book for children",
                "rating": 4
            }
        }
    }
    



BOOKS = [
    Book(1,"Computer Science Noob", "Prajwal", "Great book", 10),
    Book(2,"Social Science Noob", "Prajwal Reddy", "A very Great book", 8),
    Book(3,"History Noob", "Alice", "Just a fine book", 7),
    Book(4,"Biology Noob", "Bob", "A very very Great book", 9),
    Book(5,"Chemistry Noob", "Nathan", "Decent book", 5),
    Book(6,"Fifty shades of coding", "Reddy", "A veryyyyyy Great book", 9)
]

@app.get("/books")
def read_all_books():
    return BOOKS


# @app.post("/create-book")
# def create_book(book_request = Body()):
#     BOOKS.append(book_request)
    

@app.post("/create-book")
def create_book(book_request:BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    
    

def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    
    return book

    


