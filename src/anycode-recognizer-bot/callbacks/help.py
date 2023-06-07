from telegram import Update
from telegram.ext import ContextTypes


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
