from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from database.member_db import members
import mysql.connector
from logs.logger_config import logger


class Member(BaseModel):
    name: str
    email: str


class UpdateMember(BaseModel):
    name: str | None = None
    email: str | None = None


router = APIRouter(tags=["members"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_member(data: Member):
    logger.info("Received request to create new member")
    data = data.model_dump(exclude_unset=True)
    try:
        new_id = members.create_member(data)
    except mysql.connector.errors.IntegrityError:
        logger.error("email already taken by another member!")
        raise HTTPException(409, "email already taken by another member!")
    logger.info("Member with id %s created successfully", new_id)
    return {"message": "member created successfully!"}


@router.get("")
def get_all_members():
    logger.info("Received request to get all members")
    all_members = members.get_all_members()
    logger.info("successfully got all members")
    return all_members


@router.get("/{id}")
def get_member_by_id(id: int):
    logger.info("Received request to get member with id %s", id)
    member = members.get_member_by_id(id)
    if member is None:
        logger.error("member with id %s not found!", id)
        raise HTTPException(404, f"member with id {id} not found!")
    logger.info("successfully got member with id %s", id)
    return member


@router.patch("/{id}")
def update_member(id: int, data: UpdateMember):
    logger.info("Received request to update member with id %s", id)
    member = members.get_member_by_id(id)
    if member is None:
        logger.error("member with id %s not found!", id)
        raise HTTPException(404, f"member with id {id} not found!")

    data = data.model_dump(exclude_unset=True)
    try:
        members.update_member(id, data)
    except mysql.connector.errors.IntegrityError:
        logger.error("email already taken by another member!")
        raise HTTPException(409, "email already taken by another member!")

    logger.info("Member with id %s updated successfully", id)
    return {"message": "member updated successfully!"}


@router.patch("/{id}/deactivate")
def deactivate_member(id: int):
    logger.info("Received request to deactivate member with id %s", id)
    member = members.get_member_by_id(id)
    if member is None:
        logger.error("member with id %s not found!", id)
        raise HTTPException(404, f"member with id {id} not found!")

    members.deactivate_member(id)
    logger.info("member with id %s deactivate successfully!", id)
    return {"message": f"member with id {id} deactivated successfully!"}


@router.patch("/{id}/activate")
def activate_member(id: int):
    logger.info("Received request to activate member with id %s", id)
    member = members.get_member_by_id(id)
    if member is None:
        logger.error("member with id %s not found!", id)
        raise HTTPException(404, f"member with id {id} not found!")

    members.activate_member(id)
    logger.info("member with id %s activate successfully!", id)
    return {"message": f"member with id {id} activated successfully!"}
