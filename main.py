import asyncio
import os

from aiogram import Bot, Dispatcher, F
from dotenv import load_dotenv

from handlers.basic import get_text
from utils.log_config import setup_logger

load_dotenv()
logger = setup_logger()


async def start_bot(bot: Bot):
    await bot.send_message(os.environ.get("CHAT_ID"), text="Bot started")


async def stop_bot(bot: Bot):
    await bot.send_message(os.environ.get("CHAT_ID"), text="Bot stopped")


async def start():
    bot = Bot(token=os.environ.get("TOKEN"))
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(get_text, F.text)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close


if __name__ == "__main__":
    asyncio.run(start())
