from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import config
from sqlalchemy import text



engine = create_async_engine(
    config.database_url,  # Must start with postgresql+asyncpg://...
    echo=True
)


# async def init_db():
#     async with engine.begin() as conn:
#          statement = text("SELECT 'hello';")
         
#          result = await conn.execute(statement)
#          print(result.all())
         
async def init_db():
    async with engine.begin() as conn:  
        from src.books.models import Book  
        
        await conn.run_sync(SQLModel.metadata.create_all)  