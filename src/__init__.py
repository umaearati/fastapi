from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"Starting application...")
    await init_db()
    yield
    print(f"Application stopped")   
  

version = "v1"

app = FastAPI(
    title="Book",
    version = version,
    description="A simple book management API",
    lifespan=life_span
    )


app.include_router(book_router,prefix=f"/api/{version}/books" ,tags=["books"])

