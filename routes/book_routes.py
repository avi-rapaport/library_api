from database.book_db import books
from database.member_db import members
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str
    genre: str


class UpdateBook(BaseModel):
    title: str | None = None
    author: str | None = None
    genre: str | None = None


router = APIRouter(tags=["books"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_book(data: Book):
    data = data.model_dump(exclude_unset=True)
    books.create_book(data)
    return {"message": "book created successfully!"}


@router.get("")
def get_all_books():
    books.get_all_books()


@router.get("/{id}")
def get_book_by_id(id: int):
    book = books.get_book_by_id(id)
    if book is None:
        raise HTTPException(404, f"book with id {id} not found!")
    return book


@router.patch("/{id}")
def update_book(id: int, data: UpdateBook):
    book = books.get_book_by_id(id)
    if book is None:
        raise HTTPException(404, f"book with id {id} not found!")

    data = data.model_dump(exclude_unset=True)
    books.update_book(id, data)
    return {"message": "book updated successfully!"}


@router.patch("/{id}/borrow/{member_id}")
def borrow_book(id: int, member_id: int):
    book = books.get_book_by_id(id)
    if book is None:
        raise HTTPException(404, f"book with id {id} not found!")

    if book.get("is_available") == "False":
        raise HTTPException(400, "book is not available!")

    member = members.get_member_by_id(member_id)
    if member is None:
        raise HTTPException(404, f"member with id {member_id} not found!")

    if member.get("is_active") == "False":
        raise HTTPException(400, "member is not active!")

    books.set_available(id, False, member_id)
    members.increment_borrows(member_id)


@router.patch("/{id}/return/{member_id}")
def return_book(id: int, member_id: int):
    book = books.get_book_by_id(id)
    if book is None:
        raise HTTPException(404, f"book with id {id} not found!")

    member = members.get_member_by_id(member_id)
    if book.get("borrowd_by_member_id") != member_id:
        raise HTTPException(400, f"member with id {member_id} doesn't have this book!")

    if member.get("is_active") == "False":
        raise HTTPException(400, "member is not active!")

    books.set_available(id, True, None)
