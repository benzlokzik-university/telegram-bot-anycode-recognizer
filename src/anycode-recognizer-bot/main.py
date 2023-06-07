import logging
import os
import sqlite3
from functools import wraps

# import telegram.request
from dotenv import load_dotenv
from telegram.constants import ChatAction
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ApplicationBuilder,
)

from callbacks import *

logger = logging.getLogger(__name__)


def logger_writing(func):
    """Writes received messages to log file."""

    @wraps(func)
    async def command_func(update, context, *args, **kwargs):
        # gets message and writes it into log file using logger global object
        global logger
        logger.info(update.message)
        return await func(update, context, *args, **kwargs)

    return command_func


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            await context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id, action=action
            )
            return await func(update, context, *args, **kwargs)

        return command_func

    return decorator


send_typing_action = send_action(ChatAction.TYPING)
send_upload_photo_action = send_action(ChatAction.UPLOAD_PHOTO)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # .encode('utf-8'),
    level=logging.DEBUG,
    # filename="log/log_interesting.log",
    # filemode="w",
    encoding="utf-8",
)


def main():
    load_dotenv(dotenv_path="../../secrets/.env")
    application = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    # Connect to the SQLite database
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    start_handler = CommandHandler("start", start.start)
    help_handler = CommandHandler("help", help.user_help)

    application.add_handler(help_handler)
    application.add_handler(start_handler)

    application.add_handler(
        MessageHandler(filters.PHOTO & ~filters.COMMAND, pic_decoder.pic_decoder)
    )
    application.run_polling()


if __name__ == "__main__":
    main()
