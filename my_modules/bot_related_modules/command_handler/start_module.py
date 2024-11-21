"""
This has the logic of how to handle /start message from 
different users and groups and so on
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""

    assert update.message is not None, "update .message is not avialbe msg not"
    assert update.message.from_user is not None, "This has error with user not"

    user = update.message.from_user

    text = (
        f"Hello <b>{user.full_name}</b>"
        f"This is a simple Note Making and storing Bot, You can "
        f"make new note here and store it and later get your Note, "
        f"You can also edit your note, share your note. \n"
        f"Now this bot is in experiment, send /help to know all things. \n"
        f"Basic Note Making: /new_note"
    )
    await context.bot.send_message(user.id, text, parse_mode=ParseMode.HTML)
