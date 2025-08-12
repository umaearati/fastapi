# from fastapi import FastAPI,APIRouter,status
# from pydantic import BaseModel
# from src.books.schemas import Book
# from typing import List
# from src.db.main import get_session
# from fastapi import HTTPException, Depends
# from sqlmodel.ext.asyncio.session import AsyncSession
# from src.books.service import BookService

# book_service = BookService()
# book_router=APIRouter()


# @book_router.get("/",response_model=List[Book])
# async def get_books(session: AsyncSession = Depends(get_session)) -> List[Book]:
#     books = book_service.get_all_books(session)
#     return books


# # @book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
# # async def post_book(create_book:Book) -> Book:
# #     new_book=create_book.model_dump()
# #     books.append(new_book)
# #     return new_book

# @book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
# async def post_book(create_book:Book) -> Book:
#     new_book=create_book.model_dump()
#     books.append(new_book)
#     return new_book



# @book_router.patch("/{book_id}",response_model=Book, status_code=status.HTTP_200_OK)
# async def update_model(book_id:int,updated_book:Book) ->Book:
#     for book in books:
#         if book["id"] == book_id:
#             book["title"] = updated_book.title
#             book["author"]=updated_book.author
#             book["price"] = updated_book.price
#             book["description"] = updated_book.description
#             return book
#     return {"error": "Book not found"}  



# @book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_book(book_id:int):
#     for book in books:
#         if book["id"] == book_id:
#             books.remove(book)
#             return {}
        
        
        
        
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.schemas import BookCreateModel

from src.books.service import BookService
from src.db.main import get_session

from .schemas import Book, BookUpdateModel


book_router = APIRouter()
book_service = BookService()



@book_router.get(
    "/", response_model=List[Book]
)
async def get_all_books(
    session: AsyncSession = Depends(get_session)
):
    books = await book_service.get_all_books(session)
    return books


@book_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Book)
async def create_a_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session)) -> dict :
    
    new_book = await book_service.create_book(book_data, session)
    return new_book


@book_router.get("/{book_uid}", response_model=Book)
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
):
    book = await book_service.get_book(book_uid, session)
    if book:
        return book   # <--- Make sure you return the book here
    else:
        raise HTTPException(status_code=404, detail="Book not found")




@book_router.patch("/{book_uid}", response_model=Book)
async def update_book(
    book_uid: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session)
) -> Book:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)

    if updated_book:
        return updated_book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )



@book_router.delete(
    "/{book_uid}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session)
):
    book_deleted = await book_service.delete_book(book_uid, session)

    if book_deleted:
        return  # returns HTTP 204 No Content automatically
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
       