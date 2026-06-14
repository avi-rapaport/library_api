from database.book_db import books
from database.member_db import members
from fastapi import APIRouter, HTTPException
from logs.logger_config import logger

router = APIRouter(tags=["reports"])


@router.get("/summary")
def get_summary_reports():
    logger.info("Received request to get summary reports")
    summary = {}
    summary.update(books.count_total_books())
    summary.update(books.count_available_books())
    summary.update(books.count_borrowed_books())
    summary.update(members.count_active_members())
    logger.info("got summary reports successfully")
    return summary


@router.get("/books-by-genre")
def get_books_by_genre_report():
    logger.info("Received request to get count by genre")
    all_books = books.count_by_genre()
    logger.info("got count by genre successfully")
    return all_books


@router.get("/top-member")
def get_top_member():
    logger.info("Received request to get top member")
    if len(books.get_all_books()) == 0:
        logger.warning("there are no members in the list!")
        raise HTTPException(400, "there are no members in the list!")
    logger.info("got top member successfully")
    return members.get_top_member()
