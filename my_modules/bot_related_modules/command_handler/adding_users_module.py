"""
Here i will keep my logics of insert users into database, 
and so on
"""

import datetime

from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

from telegram import Update
from telegram.ext import ContextTypes

from my_modules.database_related_modules.database import engine
from my_modules.database_related_modules.models import UserPart


def get_current_time_ist() -> datetime.datetime:
    """Returns the current time in Indian Standard Time (IST)."""
    ist_timezone = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    now_time_ist = datetime.datetime.now(ist_timezone)
    return now_time_ist


async def add_me_to_database_cmd(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """This will trigger when user will send this /add_me_to_database to bot"""
    assert update.message is not None, "update .message is not avialbe msg not"
    assert update.message.from_user is not None, "This has error with user not"

    user = update.message.from_user
    text = f"Hello {user.full_name} I will insert your data in  our database and confirm you."

    await context.bot.send_message(
        user.id, text.upper() + "i am making ur obj instance"
    )

    user_obj = UserPart(
        user_id=user.id,
        username=user.username,
        full_name=user.full_name,
        register_time=get_current_time_ist(),
    )
    try:
        with Session(engine) as sesssion:
            sesssion.add(user_obj)
            sesssion.commit()
            sesssion.refresh(user_obj)
            print(user_obj)
    except IntegrityError as e:
        error_message = str(e.orig)

        if "user_data.user_id" in error_message:
            text = (
                f"{user.id} is already present in our database, you are already a user"
            )
            await context.bot.send_message(user.id, text)
        else:
            text = f"Here is some integrity error"
            await context.bot.send_message(user.id, text)
