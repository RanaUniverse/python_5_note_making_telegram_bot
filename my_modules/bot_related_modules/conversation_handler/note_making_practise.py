"""
Here i will make the logiccal code to take
Note title and dat to insert in my database
"""

from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)

TTILE, SUBJECT, CONFIRMATION = range(3)


async def new_note_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    This will trigger the starting callback to start title taking
    This will trigger when a user will send /new_note
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
    return TTILE


async def get_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Thsi will take a text which will be title of the note
    """
    assert update.message is not None, "Message is come with thsi update"
    assert update.message.from_user is not None, "User is associated"
    assert context.user_data is not None, "User specefic dict inbuilt"

    user = update.message.from_user
    context.user_data["title"] = update.message.text
    text = (f"Your Title i remember already now send the subject of the note below "
            "Now Send your subject of the note below  👇👇👇")
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
    return CONFIRMATION


async def confirm_ok(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
    await context.bot.send_message(user.id, text, parse_mode= "html")
    return ConversationHandler.END


# Define the handler for the conversation
new_note_handler = ConversationHandler(
    entry_points=[CommandHandler("new_note", new_note_cmd)],
    states={
        TTILE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_title)],
        SUBJECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_subject)],
        CONFIRMATION: [CommandHandler("save_note", confirm_ok)],
    },
    fallbacks=[CommandHandler("cancel", confirm_ok)],
)
