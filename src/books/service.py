from datetime import datetime

from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.models import Book
from src.books.schemas import BookCreateModel, BookUpdateModel
from datetime import datetime
import uuid


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))

        result = await session.exec(statement)

        return result.all()

    async def get_user_books(self, user_uid: str, session: AsyncSession):
        statement = (
            select(Book)
            .where(Book.user_uid == user_uid)
            .order_by(desc(Book.created_at))
        )

        result = await session.exec(statement)

        return result.all()


async def get_book(self, book_uid: str, session: AsyncSession):
    try:
        book_uuid = uuid.UUID(book_uid)  # Convert string to UUID
    except ValueError:
        return None  # If invalid UUID string, just return None

    statement = select(Book).where(Book.uid == book_uuid)
    result = await session.exec(statement)
    return result.first()



async def create_book(
    self, book_data: BookCreateModel, user_uid: str, session: AsyncSession
):
    book_data_dict = book_data.model_dump()
    book_data_dict["published_date"] = datetime.strptime(
        book_data_dict["published_date"], "%Y-%m-%d"
    )

    new_book = Book(**book_data_dict)
    new_book.user_uid = user_uid

    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)  # refresh to get updated data like generated fields

    return new_book


async def update_book(
    self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession
):
    book_to_update = await self.get_book(book_uid, session)

    if book_to_update is not None:
        update_data_dict = update_data.model_dump()

        for k, v in update_data_dict.items():
            if v is not None:
                setattr(book_to_update, k, v)

        await session.commit()
        await session.refresh(book_to_update)

        return book_to_update
    else:
        return None


async def delete_book(self, book_uid: str, session: AsyncSession):
    book_to_delete = await self.get_book(book_uid, session)

    if book_to_delete is not None:
        session.delete(book_to_delete)  # no await needed here
        await session.commit()
        return {}
    else:
        return None
