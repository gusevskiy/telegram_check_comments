import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aiogram import Bot
import asyncio
from aiogram.types import Message

from transformers import BertForSequenceClassification, BertTokenizer, pipeline
from utils.log_config import setup_logger

logger = setup_logger()


async def get_text(msg: Message, bot: Bot):
    text = msg.text
    # username = msg.from_user.username
    print(msg.message_id)
    if await model_check_text(text):
        # logger.info(msg)
        await msg.reply("You toxic, I'm blocking you")




# Загрузить модель локально
# model = pipeline("text-classification", model="cointegrated/rubert-tiny-sentiment-balanced")
# model.model.save_pretrained(r"C:\DEV_python\teelgram_check_comments\model\cointegrated_rubert-tiny-sentiment-balanced")
# model.tokenizer.save_pretrained(r"C:\DEV_python\teelgram_check_comments\model\cointegrated_rubert-tiny-sentiment-balanced")


async def model_check_text(text):
    """
    [{'label': 'toxic', 'score': 0.994674563407898}]
    """
    path_model = r"C:\DEV_python\teelgram_check_comments\model\cointegrated_rubert-tiny-sentiment-balanced"
    model = BertForSequenceClassification.from_pretrained(path_model)
    tokenizer = BertTokenizer.from_pretrained(path_model)
    nlp = pipeline("text-classification", model=model, tokenizer=tokenizer)

    sentiment = nlp(text)
    if sentiment[0].get("label") == "negative":
        return True, sentiment
    return False, sentiment


if __name__ == "__main__":
    result = asyncio.run(
        model_check_text(
            "ну и хрень тут у вас"
        )
    )
    print(result)
