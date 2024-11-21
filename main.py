"""
This is a note making app example for telegram bot related 
"""

import os

import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    # ContextTypes,
    MessageHandler,
    filters,
)

from dotenv import load_dotenv


from files.practise_file import a_conv_example, adding_users_module, new_note_module
from my_modules.bot_related_modules.command_handler import (
    start_module,
    help_module,
)
from my_modules.bot_related_modules.message_handler import text_msg_module
from my_modules.bot_related_modules.conversation_handler import (
    note_making_conversation,
)

from my_modules.database_related_modules.database import create_db_and_engine


load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.

    if BOT_TOKEN:
        application = Application.builder().token(BOT_TOKEN).build()
    else:
        application = Application.builder().token("RanaUniverse🍌🍌🍌").build()
        print("There is Not any Bot Token in the .env file, pls edit the .env file ❌")
        return None

    application.add_handler(a_conv_example.conv_handler)
    application.add_handler(a_conv_example.title_subject_handler)
    application.add_handler(note_making_conversation.new_note_handler)

    # I maybe separate the /start differnet for group and user
    application.add_handler(
        CommandHandler(
            "start",
            start_module.start_cmd,
        )
    )

    # i am thinking to make /help different for differnet user in next updates
    application.add_handler(
        CommandHandler(
            "help",
            help_module.help_cmd,
        )
    )

    # This Below will Removed in next time and add the /register
    application.add_handler(
        CommandHandler(
            command="add_me_to_database",
            callback=adding_users_module.add_me_to_database_cmd,
        )
    )

    # this will compltely removed in next time, new: /new_note
    application.add_handler(
        CommandHandler(
            "new_note_without_title",
            new_note_module.new_note_without_title,
        )
    )

    # This will also delete, but not idea what to do with this currently
    application.add_handler(
        CommandHandler(
            command="note_iformation_by_note_id",
            callback=new_note_module.note_iformation_by_note_id,
        )
    )

    # This is not need maybe delete next time
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_msg_module.echo,
        )
    )

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    create_db_and_engine()

    main()
