"""
Here will the code for answer /help 
"""

from telegram import Update
from telegram.ext import ContextTypes


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """This will execute when user will send /help"""
    assert update.message is not None, "update .message is not avialbe msg not"
    assert update.message.from_user is not None, "This has error with user not"
    
    user = update.message.from_user
    text = (
        f"Hello {user.full_name} You maybe need help, "
        "You can now use this bot to get as a note making app, there "
        "is some fetures which is developing continuously, like you can "
    )
    await context.bot.send_message(user.id, text)
