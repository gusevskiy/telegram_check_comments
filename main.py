import os

from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message

from handlers.basic import model_check_text
from utils.log_config import setup_logger

load_dotenv()
logger = setup_logger()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
chat_id = int(os.getenv('CHAT_ID'))

# client = Client(name='my_client', api_id=api_id, api_hash=api_hash)

app = Client("my_client", bot_token=os.getenv('TOKEN'))

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
        if check:
            # пишем в лог только отпределеные как негатив
            # вообще можно наверно копить таким образом dataset и потом на нем модель обучать
            # интересно
            logger.info(f"{check} -> {result} -> {message.text[:30]}")
            # предупреждение для пользователя, по идее нужно логику блокировки делать.
            await message.reply(f"{user_name} -> You toxic, I'm blocking you")
    except Exception as e:
        logger.error(f"app error: {str(e)}")


# Одно из решений чтобы бота не добавляли другие пользователи.
# по ка эффективность не понятна
@app.on_chat_member_updated()
async def check_admin_status(app, message: Message):
    chat_member = await app.get_chat_member(message.chat.id, app.me.id)
    if not chat_member.status == "administrator":
        await app.leave_chat(message.chat.id)


if __name__ == '__main__':
    app.run()
