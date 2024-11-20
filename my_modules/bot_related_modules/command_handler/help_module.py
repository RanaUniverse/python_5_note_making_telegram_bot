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
        "is some fetures which is developing continuously, like you can \n\n"
        "/add_me_to_database: and i will add you in our database "
        "/new_note_without_title write something here"
        "/note_iformation_by_note_id 999888 liek this to get the information of the note "
        "/new_note This is a insert data in a database of notes"
    )
    await context.bot.send_message(user.id, text)
