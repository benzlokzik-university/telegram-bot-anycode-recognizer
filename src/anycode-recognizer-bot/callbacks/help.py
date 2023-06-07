from telegram import Update
from telegram.ext import ContextTypes


async def user_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"""
Salut again, {update.effective_user.full_name}!
This is a bot to recognize and create barcodes, QR etc!
By default you can send a picture to decode it.
/qr — create a QR or barcode or smth like that
"""
    )
