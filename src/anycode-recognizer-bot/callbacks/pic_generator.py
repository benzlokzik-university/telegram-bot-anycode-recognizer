from io import BytesIO

from PIL import Image
from ..ImgTools import generators, signature
from telegram import Update
from telegram.ext import ContextTypes



@send_upload_photo_action
async def pic_decoder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = context.bot
    # ---
    new_image = generators.Generator(i.type, i.data.decode("utf-8")).img
    new_image = signature.SignatureAdder(new_image, font_path='ttf/Symbola.ttf')().tobytes()
    sending_image = BytesIO(new_image)
    image_file = InputFile(sending_image, "image.jpg")
    # ---
    caption = f"Detected {i.type} code!\nHere's the value:\n{i.data.decode('utf-8')}"
    print(caption)
    await bot.send_message(chat_id=update.message.chat_id, text=caption)
    # ---
    await bot.send_photo(
        chat_id=update.message.chat_id, photo=sending_image, caption=caption
    )
