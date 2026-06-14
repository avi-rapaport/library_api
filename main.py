from fastapi import FastAPI
from routes.book_routes import router as books_router
from routes.member_routes import router as members_router
from contextlib import asynccontextmanager
from database.db_connection import connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    connection.create_tables()
    yield
    connection.close()


app = FastAPI(lifespan=lifespan)

app.include_router(books_router, prefix="/books")
app.include_router(members_router, prefix="/members")
