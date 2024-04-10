import asyncio
import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
from saavn import search

TOKEN = os.getenv('TOKEN')


async def find(update,context):
    result = await search(update.message.text)
    for item in result:
        title = item.get('title')
        image = item.get('image')
        url = item.get('url')
        audio = item.get('audio')
        description = item.get('description')

        try:
            await update.message.reply_audio(
                audio = url.content,
                title = title,
                caption = description,
                thumbnail = image
                )
        except Exception as e:
            await update.message.reply_html(f"An error occurred: {e}\nAudio URL: {audio}\n<b>Title: {title}</b>\nDescription: {description}")

    await update.message.reply_text("Thanks for Using Song Downloder")


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
application = Application.builder().token(TOKEN).build()
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find))
application.run_polling(allowed_updates=Update.ALL_TYPES)

