from io import BytesIO

from PIL import Image
from ..ImgTools import reader
from telegram import Update
from telegram.ext import ContextTypes


@send_upload_photo_action
async def pic_decoder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
        print(read_data.decoded)
        for i in read_data.decoded:
            caption = (
                f"Detected {i.type} code!\nHere's the value:\n{i.data.decode('utf-8')}"
            )
            print(caption)
            await bot.send_message(chat_id=update.message.chat_id, text=caption)
