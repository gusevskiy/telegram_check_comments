'''
Для работы бота нужно поднять session
подробнее здесь https://docs.pyrogram.org/start/auth
'''
import os
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()

# api_id = 12345
# api_hash = "0123456789abcdef0123456789abcdef"
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

app = Client(name='my_client', api_id=api_id, api_hash=api_hash)

app.run()