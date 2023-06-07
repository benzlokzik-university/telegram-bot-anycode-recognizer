import sqlite3
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

# Connect to the SQLite database
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute(
    """CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY, username TEXT, message_count INTEGER, pic_count INTEGER)"""
)
conn.commit()


# SQLite function wrapper
def execute_query(query, params=()):
    cursor.execute(query, params)
    conn.commit()


def fetch_one(query, params=()):
    cursor.execute(query, params)
    return cursor.fetchone()


def fetch_all(query, params=()):
    cursor.execute(query, params)
    return cursor.fetchall()


# Define the command handlers
def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    username = update.message.from_user.username

    # Check if the user already exists in the database
    user = fetch_one("SELECT * FROM users WHERE id=?", (chat_id,))

    if user is None:
        # Insert a new user into the database
        execute_query("INSERT INTO users VALUES (?, ?, 0, 0)", (chat_id, username))

        update.message.reply_text("Welcome! You have been added to the database.")
    else:
        update.message.reply_text("Welcome back!")


def count_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    # Increment the message counter for the user
    execute_query(
        "UPDATE users SET message_count = message_count + 1 WHERE id=?", (chat_id,)
    )


def count_pic(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    # Increment the picture counter for the user
    execute_query("UPDATE users SET pic_count = pic_count + 1 WHERE id=?", (chat_id,))
