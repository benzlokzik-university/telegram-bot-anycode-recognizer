import logging
import os
from functools import wraps
from io import BytesIO

from PIL import Image
from dotenv import load_dotenv
from telegram import Update, InputFile  # , InlineKeyboardButton
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from moduls import generators, reader, signature


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return await func(update, context, *args, **kwargs)

        return command_func

    return decorator


send_typing_action = send_action(ChatAction.TYPING)
send_upload_photo_action = send_action(ChatAction.UPLOAD_PHOTO)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    # filename="log/debug.log",
    # filemode="w"
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
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Sup🖐🏿\nI'm a bot to simplify ur life. Send /help to get started"
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


@send_typing_action
async def base64_decoder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('')


@send_upload_photo_action
async def pic_decoder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file_id = update.message.photo[-1].file_id
    bot = context.bot
    file_bytes = bot.get_file(file_id)
    print(file_bytes)
    file_bytes_io = BytesIO(file_bytes)
    image = Image.open(file_bytes_io)
    read_data = reader.Decoder(image)
    if not len(read_data):
        await update.message.reply_text("""Nothing was found 🤷‍♂️\nTry again with better pic""")
    else:
        for i in read_data():
            new_image = generators.Generator(i[0], i[1]).img
            new_image = signature.SignatureAdder(new_image)().tobytes()
            sending_image = BytesIO(new_image)
            image_file = InputFile(sending_image, 'image.jpg')
            caption = f"Detected {i[0]} code!\nHere's thee value: ```{i[1]}```"
            await bot.send_photo(chat_id=update.message.chat_id, photo=image_file, caption=caption)


def main():
    load_dotenv(dotenv_path='secrets/.env')
    application = ApplicationBuilder().token(os.getenv('TOKEN')).build()

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', user_help)

    application.add_handler(help_handler)
    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, base64_decoder))
    application.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, pic_decoder))
    application.run_polling()


if __name__ == '__main__':
    main()
