import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from dotenv import load_dotenv

load_dotenv()


async def start_bot(bot: Bot):
    await bot.send_message(os.environ.get("CHAT_ID"), text="Bot started")


async def stop_bot(bot: Bot):
    await bot.send_message(os.environ.get("CHAT_ID"), text="Bot stopped")


async def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    )

    bot = Bot(token=os.environ.get("TOKEN"))
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)



    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close


if __name__ == "__main__":
    # print(os.environ.get('TOKEN'))

    asyncio.run(start())
