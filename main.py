import asyncio
import os

from dotenv import load_dotenv

import asyncio
from typing import AsyncGenerator

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

# from handlers.basic import get_text
from utils.log_config import setup_logger

load_dotenv()
logger = setup_logger()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
chat_id = int(os.getenv('CHAT_ID'))

# client = Client(name='my_client', api_id=api_id, api_hash=api_hash)

app = Client("my_client")

@app.on_message(filters.chat(chats=chat_id))
async def get_message(client, message):
    logger.info(message.text)
    await message.reply(message.text)


if __name__ == '__main__':
    app.run()
