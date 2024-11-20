"""
This is the engine part having the engine to use
and it will have a table making fun
"""

from pathlib import Path

from sqlmodel import (
    create_engine,
    SQLModel,
)


# sqlite_file_name = Path("my_files") / "database.db"
sqlite_file_name = Path.cwd() / "database.db"

sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(url=sqlite_url)


def create_db_and_engine():
    sqlite_file_name.parent.mkdir(exist_ok=True)
    SQLModel.metadata.create_all(engine)