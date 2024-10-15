import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, Message

from handlers.basic import model_check_text
from utils.log_config import setup_logger

load_dotenv()
logger = setup_logger()

chat_id = int(os.getenv("CHAT_ID"))
block_time_hour = int(os.getenv("BLOCK_TIME_HOUR"))
token = os.getenv("TOKEN")



# предварительно запустить файл add_session.py 
app = Client("utils/my_client", bot_token=token)

user_warnings = {}

async def work_block(app, toxic_user_id):
    # вообще можно наверно копить таким образом dataset и потом на нем модель обучать
    # интересно
    # блокируем человека на указанное время
    await app.restrict_chat_member(
        chat_id,
        user_id=toxic_user_id,
        permissions=ChatPermissions(),
        until_date=datetime.now() + timedelta(hour=block_time_hour),
    )


@app.on_message(filters.chat(chats=chat_id))
async def get_message(app, message: Message):
    """
    Приложение мониторит группу chat_id
    каждое сообщение отправляет в модель
    Блокирует пользователя если он шлет негативные комментарии
    """
    try:
        # получаем результат от модели
        check, result = await model_check_text(message.text)
        # У некоторых пользователей нет username, тч лучше использовать имя
        user_name = message.from_user.first_name
        user_id = message.from_user.id
        if check:
            # пишем в лог только отпределеные как негатив
            logger.info(f"{check} -> {result} -> {message.text[:30]}")
            # к предупреждениям пользователя прибавляем score
            warnings = user_warnings.get(user_id, 0) + result[0].get("score")
            # в словарь user_warnings добавляем обновленное значение
            user_warnings[user_id] = warnings

            if warnings >= 3:
                # обнуляем счетчик (как тут поступать вопрос открытый)
                user_warnings[user_id] = 0
                logger.info(f"{user_name} - {user_id} blocked")
                # блокируем
                await message.reply(f"{user_name} -> You toxic, I'm blocking you")
                await work_block(app, user_id)
            else:
                await message.reply(
                    f"{user_name} -> Warning!!! You message toxic on {int(result[0].get("score")*100)}%"
                )
    except Exception as e:
        logger.error(f"app error: {str(e)}")


if __name__ == "__main__":
    app.run()
