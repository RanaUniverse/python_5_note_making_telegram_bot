"""
This is a note making app example for telegram bot related 
"""

import os

import logging

from telegram import  Update
from telegram.ext import (
    Application,
    CommandHandler,
    # ContextTypes,
    MessageHandler,
    filters,
)

from dotenv import load_dotenv


from my_modules.bot_related_modules.command_handler import start_module, help_module
from my_modules.bot_related_modules.message_handler import text_msg_module
load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.

\


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.

    if BOT_TOKEN:
        application = Application.builder().token(BOT_TOKEN).build()
    else:
        application = Application.builder().token("RanaUniverse🍌🍌🍌").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start_module.start_cmd))
    application.add_handler(CommandHandler("help", help_module.help_cmd))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_msg_module.echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
