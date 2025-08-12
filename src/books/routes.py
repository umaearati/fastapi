from fastapi import FastAPI,APIRouter
from pydantic import BaseModel
from src.books.schemas import Book
from typing import List
from src.books.book_data import books

book_router=APIRouter()


@book_router.get("/",response_model=List[Book])
async def get_books():
    return books


@book_router.post("/", response_model=Book)
async def post_book(create_book:Book) -> Book:
    new_book=create_book.model_dump()
    books.append(new_book)
    return new_book


@book_router.patch("/{book_id}",response_model=Book)
async def update_model(book_id:int,updated_book:Book) ->Book:
    for book in books:
        if book["id"] == book_id:
            book["title"] = updated_book.title
            book["author"]=updated_book.author
            book["price"] = updated_book.price
            book["description"] = updated_book.description
            return book
    return {"error": "Book not found"}  



@book_router.delete("/{book_id}")
async def delete_book(book_id:int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {}