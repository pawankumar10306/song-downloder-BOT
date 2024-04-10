import os
import logging
from saavn import search
import asyncio

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response
from starlette.routing import Route

from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    filters,
    MessageHandler,
)

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



# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Define configuration constants
URL = os.environ.get("RENDER_EXTERNAL_URL")  # NOTE: We need to tell telegram where to reach our service
PORT = 8000


async def main() -> None:
    """Set up PTB application and a web application for handling the incoming requests."""
    application = (
        Application.builder().token(TOKEN).updater(None).build()
    )

    # register handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find))

    # Pass webhook settings to telegram
    await application.bot.set_webhook(url=f"{URL}/telegram", allowed_updates=Update.ALL_TYPES)

    # Set up webserver
    async def telegram(request: Request) -> Response:
        """Handle incoming Telegram updates by putting them into the `update_queue`"""
        await application.update_queue.put(
            Update.de_json(data=await request.json(), bot=application.bot)
        )
        return Response()

    async def health(_: Request) -> PlainTextResponse:
        """For the health endpoint, reply with a simple plain text message."""
        return PlainTextResponse(content="The bot is still running fine :)")

    starlette_app = Starlette(
        routes=[
            Route("/telegram", telegram, methods=["POST"]),
            Route("/healthcheck", health, methods=["GET"]),
        ]
    )
    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=starlette_app,
            port=PORT,
            use_colors=False,
            host="0.0.0.0",  # NOTE: Render requires you to bind your webserver to 0.0.0.0
        )
    )

    # Run application and webserver together
    async with application:
        await application.start()
        await webserver.serve()
        await application.stop()


if __name__ == "__main__":
    asyncio.run(main())