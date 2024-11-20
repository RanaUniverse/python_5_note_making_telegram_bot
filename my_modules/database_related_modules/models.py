"""
This is the file where i will keep my table structers
"""

import datetime

from sqlmodel import (
    Field,  # type: ignore
    # Relationship,
    SQLModel,
)


class UserPart(SQLModel, table=True):
    __tablename__: str = "user_data"  # type: ignore

    id_: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(index=True, unique=True)
    username: str | None = Field(default=None, index=True)
    full_name: str | None = Field(default=None)

    email_id: str | None = Field(default=None)
    phone_no: str | None = Field(default=None)
    register_time: datetime.datetime | None = Field(default=None)
    notes_count: int | None = Field(default=None)
    is_allowed: bool = Field(default=True)
    password: str | None = Field(default=None)


class NotePart(SQLModel, table=True):
    __tablename__: str = "note_data"  # type: ignore

    id_: int = Field(default=None, primary_key=True)

    title: str | None = Field(default=None)
    subject: str | None = Field(default=None)

    note_id: int | None = Field(default=None, unique=True)
    created_date: datetime.datetime | None = Field(default=None)
    edited_date: datetime.datetime | None = Field(default=None)

    user_id: int | None = Field(default=None, foreign_key="user_data.user_id")
