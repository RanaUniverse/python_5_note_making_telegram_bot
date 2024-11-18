# pyright: ignore


"""
This has the logic of how to handle /start message from 
different users and groups and so on
"""

from telegram import Update
from telegram.ext import ContextTypes


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  # type: ignore
    """Send a message when the command /start is issued."""

    assert update.message is not None, "update .message is not avialbe msg not"
    assert update.message.from_user is not None, "This has error with user not"

    user = update.message.from_user

    # text = (
    #     f"Hello {user.full_name} You Have just started this bot,"
    #     "What do you want from me get /help to know more"
    # )
    text = (
        f"This is a Note making and storing applicatioin bot, i am making "
        "this bot to learn how to use database to store data and retrieve in future "
        "you can use /help to see how to use different thigns ,\n"
        "First things is i need user registration, and then you can make new note "
        "you need to pass title and subject to keep starting store your data."
    )
    await context.bot.send_message(user.id, text)
