"""
This is frist for practise this will trigger when user will send
/a 
this will satrt some asking and so on
"""

import logging

from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    filters,
    ConversationHandler,
    MessageHandler,
)


GENDER, PHOTO, LOCATION, BIO = range(4)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Boy", "Girl", "Other"]]

    await update.message.reply_text(
        "Hi! My name is Professor Bot. I will hold a conversation with you. "
        "Send /cancel to stop talking to me.\n\n"
        "Are you a boy or a girl?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Boy or Girl?",
        ),
    )

    return GENDER


async def help_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """This is alos for /helps_conversation to start the conversation"""
    user = update.message.from_user
    text = f"You have press help and you need help but for example i am sending you back teh gender choose"
    await context.bot.send_message(user.id, text)
    return GENDER


async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "I see! Please send me a photo of yourself, "
        "so I know what you look like, or send /skip if you don't want to.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive("user_photo.jpg")
    logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
    await update.message.reply_text(
        "Gorgeous! Now, send me your location please, or send /skip if you don't want to."
    )

    return LOCATION


async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    await update.message.reply_text(
        "I bet you look great! Now, send me your location please, or send /skip."
    )

    return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f",
        user.first_name,
        user_location.latitude,
        user_location.longitude,
    )
    await update.message.reply_text(
        "Maybe I can visit you sometime! At last, tell me something about yourself."
    )

    return BIO


async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    await update.message.reply_text(
        "You seem a bit paranoid! At last, tell me something about yourself."
    )

    return BIO


async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text("Thank you! I hope we can talk again some day.")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start_conversation", start),
        CommandHandler("helps_conversation", help_conversation),
    ],
    states={
        GENDER: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), gender)],
        PHOTO: [
            MessageHandler(filters.PHOTO, photo),
            CommandHandler("skip", skip_photo),
        ],
        LOCATION: [
            MessageHandler(filters.LOCATION, location),
            CommandHandler("skip", skip_location),
        ],
        BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)


TITLE, SUBJECT = range(2)


async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts a new conversation to ask for a title and subject."""
    await update.message.reply_text(
        "Let's begin! Please provide a title for your input."
    )
    return TITLE


async def get_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the title and asks for the subject."""
    user = update.message.from_user
    context.user_data["title"] = update.message.text
    logger.info("Title from %s: %s", user.first_name, context.user_data["title"])
    await update.message.reply_text("Got it! Now, please provide the subject.")
    return SUBJECT


async def get_subject(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the subject and ends the conversation."""
    user = update.message.from_user
    context.user_data["subject"] = update.message.text
    logger.info("Subject from %s: %s", user.first_name, context.user_data["subject"])
    await update.message.reply_text(
        f"Thank you! Here's what you provided:\n\n"
        f"**Title**: {context.user_data['title']}\n"
        f"**Subject**: {context.user_data['subject']}\n\n"
        "I hope this was helpful!"
    )
    return ConversationHandler.END


async def cancel_title_subject(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Cancels and ends the title and subject conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the title and subject input.", user.first_name)
    await update.message.reply_text(
        "No problem! Let me know if you need help with something else.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


# Add the new ConversationHandler
title_subject_handler = ConversationHandler(
    entry_points=[CommandHandler("a", command_handler)],
    states={
        TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_title)],
        SUBJECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_subject)],
    },
    fallbacks=[CommandHandler("cancel", cancel_title_subject)],
)
