"""
THis module is for taking inputs from user and then make
a note saving in our database.
"""

import datetime

from sqlmodel import Session
from telegram import Update
from telegram.ext import (
    filters,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
)

from my_modules.database_related_modules.database import engine
from my_modules.database_related_modules.models import NotePart


def get_current_time_ist() -> datetime.datetime:
    """Returns the current time in Indian Standard Time (IST)."""
    ist_timezone = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    now_time_ist = datetime.datetime.now(ist_timezone)
    return now_time_ist


TITLE, SUBJECT, CONFIRM = range(3)


async def new_note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    /new_note when user will send this note making will start
    """

    assert update.message is not None, "Message is come with thsi update"
    assert update.message.from_user is not None, "User is associated"

    user = update.message.from_user
    text = (
        f"You Can Now Make new Note here, i will keep the note in my database "
        "and your data will be saved in our database, and you can also get them. "
        "Please Send Your Title of the Note 👇👇👇"
    )
    await context.bot.send_message(user.id, text)
    return TITLE


async def get_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This fun will execute when i will send text to save as a title
    """
    assert update.message is not None, "Message is come with thsi update"
    assert update.message.from_user is not None, "User is associated"
    assert context.user_data is not None, "User specefic dict inbuilt"

    user = update.message.from_user
    context.user_data["title"] = update.message.text
    text = (
        f"Your Title i remember already now send the subject of the note below "
        "Now Send your subject of the note below  👇👇👇"
    )
    await context.bot.send_message(user.id, text)
    return SUBJECT


async def get_subject(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This will take the subject of the note and save in next function
    """
    assert update.message is not None, "Message is come with thsi update"
    assert update.message.from_user is not None, "User is associated"
    assert context.user_data is not None, "User specefic dict inbuilt"

    user = update.message.from_user
    context.user_data["subject"] = update.message.text
    text = (
        f"You have successfully send both title and subject of your note "
        f"If you want to see the note just press /save_note"
    )
    await context.bot.send_message(user.id, text)
    return CONFIRM


async def save_note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This will just end the convirmation here
    this will execute when user will lastly send /save_note
    """
    assert update.message is not None, "Message is come with thsi update"
    assert update.message.from_user is not None, "User is associated"
    assert context.user_data is not None, "User specefic dict inbuilt"

    user = update.message.from_user
    text = (
        f"YOu have send /save_note now your note is saved, "
        "But still now i have not make any backednd to save thsi note ❌\n\n"
        f"<b>TITLE</b>: {context.user_data.get("title")}\n\n"
        f"<b>SUBJECT</b>: {context.user_data.get("subject")}"
    )
    await context.bot.send_message(user.id, text, parse_mode="html")

    note_obj = NotePart(
        title=context.user_data.get("title"),
        subject=context.user_data.get("subject"),
        note_id=int(update.message.date.timestamp()),
        created_date=get_current_time_ist(),
        user_id=update.message.from_user.id,
    )

    try:
        with Session(engine) as session:
            session.add(note_obj)
            session.commit()
        text = f"Your Note has been inserted into the database successfully"
        await context.bot.send_message(user.id, text)

    except Exception as e:
        text = (
            f"Here is some problem to save thsi in the database"
            f"Please send this screenshot to the admin: "
            f"{e}"
        )
        await context.bot.send_message(user.id, text)

    return ConversationHandler.END


async def cancel_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This will cancel the note-making process.
    """
    assert update.message is not None, "Message is come with thsi update"
    assert update.message.from_user is not None, "User is associated"

    user = update.message.from_user
    text = (
        "The note-making process has been cancelled. If you want to start again, "
        "just send /new_note."
    )
    await context.bot.send_message(user.id, text)
    return ConversationHandler.END


# Define the handler for the conversation
new_note_handler = ConversationHandler(
    entry_points=[CommandHandler("new_note", new_note_cmd)],
    states={
        TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_title)],
        SUBJECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_subject)],
        CONFIRM: [CommandHandler("save_note", save_note_cmd)],
    },
    fallbacks=[CommandHandler("cancel", cancel_cmd)],
)
