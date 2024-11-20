from sqlmodel import Session

from my_modules.database_related_modules.database import create_db_and_engine, engine
from my_modules.database_related_modules.models import UserPart, NotePart



# Example user 5
user5 = UserPart(
    user_id=6,
    username="lisa_j",
    full_name="Lisa Johnson",
    email_id="lisa.johnson@example.com",
    phone_no="9098765432",
    password="lisa_secure#321",
)


# Example note 1
note1 = NotePart(
    title="Meeting Notes",
    subject="Project Planning",
    note_id=2001,
    user_id=2,  # Belongs to user with user_id=2
)


def insert_data():
    with Session(engine) as session:
        # Example user

        session.add(user5)
        session.commit()

        # Example note

        session.add(note1)
        session.commit()


if __name__ == "__main__":
    create_db_and_engine()
    insert_data()