from database.book_db import books
from database.member_db import members
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from logs.logger_config import logger
from enum import Enum


class Genre(str, Enum):
    FICTION = "Fiction"
    NON_FICTION = "Non-fiction"
    SCIENCE = "Science"
    HISTORY = "History"
    OTHER = "Other"


class Book(BaseModel):
    title: str
    author: str
    genre: Genre


class UpdateBook(BaseModel):
    title: str | None = None
    author: str | None = None
    genre: Genre | None = None


router = APIRouter(tags=["books"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_book(data: Book):
    logger.info("Received request to create new book")
    data = data.model_dump(exclude_unset=True)
    new_id = books.create_book(data)
    logger.info("Book with id %s created successfully", new_id)
    return {"message": f"Book with id {new_id} created successfully!"}


@router.get("")
def get_all_books():
    logger.info("Received request to get all books")
    all_books = books.get_all_books()
    logger.info("successfully got all books")
    return all_books


@router.get("/{id}")
def get_book_by_id(id: int):
    logger.info("Received request to get book with id %s", id)
    book = books.get_book_by_id(id)
    if book is None:
        raise HTTPException(404, f"book with id {id} not found!")
    logger.info("successfully got book with id %s", id)
    return book


@router.patch("/{id}")
def update_book(id: int, data: UpdateBook):
    logger.info("Received request to update book with id %s", id)
    book = books.get_book_by_id(id)
    if book is None:
        raise HTTPException(404, f"book with id {id} not found!")

    data = data.model_dump(exclude_unset=True)
    books.update_book(id, data)
    logger.info("successfully updated book with id %s", id)
    return {"message": "book updated successfully!"}


@router.patch("/{id}/borrow/{member_id}")
def borrow_book(id: int, member_id: int):
    logger.info("Received request to borrow book with id %s", id)
    book = books.get_book_by_id(id)
    if book is None:
        logger.error("book with id %s not found!", id)
        raise HTTPException(404, f"book with id {id} not found!")

    if book.get("is_available") == False:
        logger.error("book is not available!")
        raise HTTPException(400, "book is not available!")

    member = members.get_member_by_id(member_id)
    if member is None:
        logger.error("member with id %s not found!", member_id)
        raise HTTPException(404, f"member with id {member_id} not found!")

    if member.get("is_active") == False:
        logger.error("member with id %s not active!", member_id)
        raise HTTPException(400, "member is not active!")

    if books.count_active_borrows_by_member(member_id) >= 3:
        logger.error("member has reached maximum borrows!")
        raise HTTPException(400, "member has reached maximum borrows!")

    books.set_available(id, False, member_id)
    members.increment_borrows(member_id)
    logger.info("book with id %s successfully borrowd to member %s", id, member_id)
    return {"message": f"book with id {id} successfully borrowd to member {member_id}"}


@router.patch("/{id}/return/{member_id}")
def return_book(id: int, member_id: int):
    logger.info("Received request to return book with id %s", id)
    book = books.get_book_by_id(id)
    if book is None:
        logger.error("book with id %s not found!", id)
        raise HTTPException(404, f"book with id {id} not found!")

    if book.get("is_available") == True:
        logger.error("book is not borrowed!")
        raise HTTPException(400, "book is not borrowed!")

    member = members.get_member_by_id(member_id)
    if member is None:
        logger.error("member with id %s not found!", id)
        raise HTTPException(404, f"member with id {member_id} not found!")

    if book.get("borrowed_by_member_id") != member_id:
        logger.error("book is not borrowed by member with id %s", member_id)
        raise HTTPException(
            400, f"book is not borrowed by member with id {member_id} !"
        )

    books.set_available(id, True, None)
    logger.info("book with id %s successfully returned from member %s", id, member_id)
    return {"message": f"book with id {id} successfully return from member {member_id}"}
