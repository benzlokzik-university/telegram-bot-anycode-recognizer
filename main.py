import logging
import os
from functools import wraps
from io import BytesIO

# import telegram.request
from PIL import Image
from dotenv import load_dotenv
from telegram import Update, InputFile  # , InlineKeyboardButton
from telegram.constants import ChatAction
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ApplicationBuilder,
)

from modules import generators, reader, signature

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
    level=logging.INFO,
    # filename="log/log.log",
    # filemode="w",
    encoding="utf-8",
)


# TODO: доделать функцию для кастом-клавы
# TODO: придумать перевод с одного языка на другой, ну или хотя бы на англ норм сделать
# def build_menu(
#         buttons: List[InlineKeyboardButton],
#         n_cols: int,
#         header_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]] = None,  # первая строка
#         footer_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]] = None  # последняя строка в клаве
# ) -> List[List[InlineKeyboardButton]]:
#     menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
#     if header_buttons:
#         menu.insert(0, header_buttons if isinstance(header_buttons, list) else [header_buttons])
#     if footer_buttons:
#         menu.append(footer_buttons if isinstance(footer_buttons, list) else [footer_buttons])
#     return menu

# barcode.EAN8('1224545', writer=barcode.writer.ImageWriter()).save('ean8test')

# TODO: добавить приветствие после старта и выбор языка через
#  https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#build-a-menu-with-buttons=
@logger_writing
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sup🖐🏿\nI'm a bot to simplify ur life. Send /help to get started",
    )


# @send_typing_action
# async def user_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     # print(dir(update.effective_user))
#     await update.message.reply_text(
#         f"""
# Salut again, {update.effective_user.full_name}!
# This is a bot to recognize and create barcodes, QR and base64 codes!
# By default, you can send a picture to decode it or .txt/text if it's a base64
# /qr — create a QR
# /base64 — encrypt w/ base64
# """
#     )


@send_typing_action
@logger_writing
async def user_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"""
Salut again, {update.effective_user.full_name}!
This is a bot to recognize and create barcodes, QR and base64 codes!
By default you can send a picture to decode it.
/qr — create a QR
/base64 — encode w/ base64
"""
    )


@logger_writing
@send_typing_action
async def base64_decoder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Should be added soon 👀")


@logger_writing
@send_upload_photo_action
async def pic_decoder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.message)
    file_id = update.message.photo[-1].file_id
    bot = context.bot

    file_obj = await bot.get_file(file_id)
    file_data = await file_obj.download_as_bytearray()

    file_bytes_io = BytesIO(file_data)
    image = Image.open(file_bytes_io)
    read_data = reader.Decoder(image)
    if not read_data:
        await update.message.reply_text(
            """Nothing was found 🤷‍♂️\nTry again with better pic"""
        )
    else:
        for i in read_data.decoded:
            caption = f"Detected {i.type} code!\nHere's the value:\n{i.data.decode('utf-8')}"
            print(caption)
            await bot.send_message(chat_id=update.message.chat_id, text=caption)
            # ---
            # new_image = generators.Generator(i.type, i.data.decode("utf-8")).img
            # new_image = signature.SignatureAdder(new_image, font_path='ttf/Symbola.ttf')().tobytes()
            # sending_image = BytesIO(new_image)
            # image_file = InputFile(sending_image, "image.jpg")
            # # ---
            # caption = f"Detected {i.type} code!\nHere's the value:\n{i.data.decode('utf-8')}"
            # print(caption)
            # await bot.send_message(chat_id=update.message.chat_id, text=caption)
            # # ---
            # await bot.send_photo(
            #     chat_id=update.message.chat_id, photo=sending_image, caption=caption
            # )


def main():
    load_dotenv(dotenv_path="secrets/.env")
    application = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", user_help)

    application.add_handler(help_handler)
    application.add_handler(start_handler)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, base64_decoder)
    )
    application.add_handler(
        MessageHandler(filters.PHOTO & ~filters.COMMAND, pic_decoder)
    )
    application.run_polling()


if __name__ == "__main__":
    main()
