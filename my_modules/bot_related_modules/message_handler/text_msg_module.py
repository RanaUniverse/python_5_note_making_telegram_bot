"""
This is the module to control the flow of text messsage comign from users
"""

from telegram import Update
from telegram.ext import ContextTypes


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    assert update.message is not None, "update .message is not avialbe msg not"
    assert update.message.from_user is not None, "This has error with user not"
    assert update.message.text is not None, "No text got"
    
    user = update.message.from_user
    text = update.message.text
    await context.bot.send_message(user.id, text.upper())
    await update.message.reply_text(update.message.text)
