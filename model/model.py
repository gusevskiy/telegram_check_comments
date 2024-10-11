# from aiogram.types import Message
# from aiogram import Bot

# Загрузить модель локально
# model = pipeline("text-classification", model="cointegrated/rubert-tiny-sentiment-balanced")
# model.model.save_pretrained(r"C:\DEV_python\teelgram_check_comments\model\cointegrated_rubert-tiny-sentiment-balanced")
# model.tokenizer.save_pretrained(r"C:\DEV_python\teelgram_check_comments\model\cointegrated_rubert-tiny-sentiment-balanced")

import asyncio
import logging

from transformers import BertForSequenceClassification, BertTokenizer, pipeline

path_model = r"C:\DEV_python\teelgram_check_comments\model\cointegrated_rubert-tiny-sentiment-balanced"

model = BertForSequenceClassification.from_pretrained(path_model)
tokenizer = BertTokenizer.from_pretrained(path_model)

nlp = pipeline("text-classification", model=model, tokenizer=tokenizer)


async def model_check_text(text: str):
    """[{'label': 'toxic', 'score': 0.994674563407898}]"""
    sentiment = nlp(text)
    # print(sentiment)
    if sentiment[0].get("label") == "negative":
        logging.info(sentiment)
        return True
    return False


if __name__ == "__main__":
    result = asyncio.run(
        model_check_text(
            "Теперь, чтобы загрузить модель из сохранённой папки, вы можете сделать следующее:"
        )
    )
    # print(result)
