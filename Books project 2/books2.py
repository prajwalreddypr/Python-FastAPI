from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int
    
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
        
class BookRequest(BaseModel):
    id: Optional[int] = Field(description = "ID is not needed on create", default = None)
    title: str = Field(min_length = 3)
    author: str = Field(min_length = 1)
    description: str = Field(min_length = 1, max_length = 10000)
    rating: int = Field(gt=0, lt=5)
    published_date: int = Field(gt = 1995, lt = 2020)
    
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "New Book",
                "author": "Prajwal Reddy",
                "description": "History book for children",
                "rating": 4,
                "published_date": 2020
            }
        }
    }
    



BOOKS = [
    Book(1,"Computer Science Noob", "Prajwal", "Great book", 10, 2012),
    Book(2,"Social Science Noob", "Prajwal Reddy", "A very Great book", 8, 2013),
    Book(3,"History Noob", "Alice", "Just a fine book", 7, 2012),
    Book(4,"Biology Noob", "Bob", "A very very Great book", 9, 2016),
    Book(5,"Chemistry Noob", "Nathan", "Decent book", 5, 2017),
    Book(6,"Fifty shades of coding", "Reddy", "A veryyyyyy Great book", 9, 2015)
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
    
    
#endpoint to fetch the book by ID  
@app.get("/book/{book_id}")
async def read_book(book_id: int = Path(gt = 0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
        
    raise HTTPException(status_code = 404, detail = "item not found" )


#endppoint to fetch the book by published_date
@app.get("/books/{published_date}")
async def by_published_date(published_date: int = Path(gt = 2000)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


    
#endpoint to fetch book by rating
@app.get("/books/{rating}")
async def book_rating(rating: int = Path(gt = 0)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return


#PUT METHODS
@app.put("/books/update_book")
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
            
    if not book_changed:
        raise HTTPException(status_code = 404, detail = "Item not found")
            

#DELETE METHODS
@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt = 0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
        
    if not book_changed: 
        raise HTTPException(status_code = 404, detail = "Item not found.")
        
        


def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    
    return book

    


