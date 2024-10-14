import os

from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.types import ChatPermissions
from datetime import datetime, timedelta

from handlers.basic import model_check_text
from utils.log_config import setup_logger

load_dotenv()
logger = setup_logger()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
chat_id = int(os.getenv("CHAT_ID"))
block_time_hour = os.getenv("BLOCK_TIME_HOUR")


# client = Client(name='my_client', api_id=api_id, api_hash=api_hash)

app = Client("my_client", bot_token=os.getenv("TOKEN"))


# async def work_block(app, message):



@app.on_message(filters.chat(chats=chat_id))
async def get_message(app, message: Message):
    """
    Приложение мониторит группу chat_id
    каждое сообщение отправляет в модель
    """
    try:
        # получаем результат от модели
        check, result = await model_check_text(message.text)
        # У некоторых пользователей нет username, тч лучше использовать имя
        user_name = message.from_user.first_name
        user_id = message.from_user.id
        if check:
            # пишем в лог только отпределеные как негатив
            # вообще можно наверно копить таким образом dataset и потом на нем модель обучать
            # интересно
            logger.info(f"{check} -> {result} -> {message.text[:30]}")
            # предупреждение для пользователя, по идее нужно логику блокировки делать.
            await message.reply(f"{user_name} -> You toxic, I'm blocking you")
            # блокируем человека на 2 минуты
            await app.restrict_chat_member(
                chat_id,
                user_id,
                ChatPermissions(),
                datetime.now() + timedelta(minutes=block_time_hour),
            )
    except Exception as e:
        logger.error(f"app error: {str(e)}")


if __name__ == "__main__":
    app.run()
