from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from database.member_db import members
import mysql.connector


class Member(BaseModel):
    name: str
    email: str


class UpdateMember(BaseModel):
    name: str | None = None
    email: str | None = None


router = APIRouter(tags=["members"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_member(data: Member):
    data = data.model_dump(exclude_unset=True)
    try:
        members.create_member(data)
    except mysql.connector.errors.IntegrityError:
        raise HTTPException(409, "email already taken by another member!")
    return {"message": "member created successfully!"}


@router.get("")
def get_all_members():
    return members.get_all_members()


@router.get("/{id}")
def get_member_by_id(id: int):
    member = members.get_member_by_id(id)
    if member is None:
        raise HTTPException(404, f"member with id {id} not found!")
    return member


@router.patch("/{id}")
def update_member(id: int, data: UpdateMember):
    member = members.get_member_by_id(id)
    if member is None:
        raise HTTPException(404, f"member with id {id} not found!")

    data = data.model_dump(exclude_unset=True)
    members.update_member(id, data)
    return {"message": "member updated successfully!"}


@router.patch("/{id}/deactivate")
def deactivate_member(id: int):
    member = members.get_member_by_id(id)
    if member is None:
        raise HTTPException(404, f"member with id {id} not found!")

    members.deactivate_member(id)
    return {"message": f"member with id {id} deactivated successfully!"}


@router.patch("/{id}/activate")
def activate_member(id: int):
    member = members.get_member_by_id(id)
    if member is None:
        raise HTTPException(404, f"member with id {id} not found!")

    members.activate_member(id)
    return {"message": f"member with id {id} activated successfully!"}
