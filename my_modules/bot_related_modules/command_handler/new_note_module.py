"""
This module is for user want to insert new note
fisrt i will make /new_note_without_title write somethign,
then it will isnert this note as subject 
"""

import datetime
from sqlmodel import Session, select

from telegram import Update
from telegram.ext import ContextTypes


from my_modules.database_related_modules.models import NotePart
from my_modules.database_related_modules.database import engine


def get_current_time_ist() -> datetime.datetime:
    """Returns the current time in Indian Standard Time (IST)."""
    ist_timezone = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    now_time_ist = datetime.datetime.now(ist_timezone)
    return now_time_ist


async def new_note_without_title(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """This will trigger when this command will come i except some subject will come with this"""
    assert update.message is not None, "update .message is not avialbe msg not"
    assert update.message.from_user is not None, "This some wrong"
    assert update.message.text is not None, "Text is coming  with command handler"
    assert update.message.from_user.full_name is not None, "user must has some name"

    user = update.message.from_user

    note_subject = update.message.text.split(maxsplit=1)[1]
    await context.bot.send_message(user.id, note_subject)

    note_obj = NotePart(
        title=f"{user.full_name} Make this note",
        subject=note_subject,
        note_id=int(update.message.date.timestamp()),
        created_date=get_current_time_ist(),
        user_id=user.id,
    )
    try:
        with Session(engine) as session:
            session.add(note_obj)
            session.commit()
            session.refresh(note_obj)

        text = f"Your Note has been saved with the note id: {note_obj.note_id}"
        await context.bot.send_message(user.id, text)
    except Exception as e:
        await context.bot.send_message(
            user.id,
            (
                "Sorry, something went wrong here. Please contact an admin and "
                "share this screenshot with them:\n\n\n"
                f"{e}"
            ),
        )


async def note_iformation_by_note_id(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    This will give teh note information if the same user made this note in past
    """
    assert update.message is not None, "update .message is not avialbe msg not"
    assert update.message.from_user is not None, "This some wrong"
    assert update.message.text is not None, "Text is coming  with command handler"
    assert update.message.from_user.full_name is not None, "user must has some name"
    assert context.args is not None, "must be some thigns "

    user = update.message.from_user

    # If user send many arguments there it will inform user the right thigns
    # text = (
    #     f"YOu have send me total {len(context.args)} numbers of words after the command"
    # )
    # await context.bot.send_message(user.id, text)

    if len(context.args) == 0:
        text = (
            "You need to pass the note ID after the command. "
            "The note ID is provided to you when you create a note."
        )
        await context.bot.send_message(user.id, text)
        return None

    elif len(context.args) > 1:
        text = (
            "You must pass only one integer value for the note ID. "
            "Multiple words are not allowed."
        )
        await context.bot.send_message(user.id, text)
        return None

    else:
        try:
            note_id = int(context.args[0])
            text = (
                f"You have provided a valid note ID: {note_id}. "
                "Fetching the note information..."
            )
            await context.bot.send_message(user.id, text)
        except ValueError:
            text = (
                "The note ID must be a valid integer. Please try again "
                "with the correct format."
            )
            await context.bot.send_message(user.id, text)
            return None

    # Now i will werite code for search if the note id is correct or not

    with Session(engine) as session:
        statement = select(NotePart).where(NotePart.note_id == note_id)
        note_row = session.exec(statement).first()
        if not note_row:
            text = (
                f"This {note_id} which you send is invalid note id this is not exists."
            )

        elif note_row.user_id != user.id:
            text = f"This note doesn't belongs to you ❌"

        elif note_row.user_id == user.id:
            text = f"YOu made this note thanks ✅"

        else:
            text = f"There are some errro with this problem ⚠️"

        await context.bot.send_message(user.id, text)
