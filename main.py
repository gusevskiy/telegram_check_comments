import asyncio
import os

from aiogram import Bot, Dispatcher, F
# from aiogram.types import ChatType
from dotenv import load_dotenv

from handlers.basic import get_text
from utils.log_config import setup_logger

load_dotenv()
logger = setup_logger()

# print(os.getenv('CHAT_ID'))

async def start_bot(bot: Bot):
    await bot.send_message(chat_id=os.environ.get("CHAT_ID"), text="Bot started")
    logger.info(f"Bot started {os.getenv("CHAT_ID")}")


async def stop_bot(bot: Bot):
    await bot.send_message(os.getenv("CHAT_ID"), text="Bot stopped")


async def start():
    # logger.info("Starting bot")
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # dp.message.register(get_text, F.chat.id == -1001847140757)

    dp.channel_post.register(get_text, F.text)
    # dp.message.register(get_text, F.)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
