from aiogram import Bot
from aiogram.types import Message

from model.model import model_check_text


async def get_text(msg: Message, bot: Bot):
    text = msg.text

    if model_check_text(text):
        await msg.answer("You toxic, I'm blocking you")
