import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio

from transformers import BertForSequenceClassification, BertTokenizer, pipeline

from utils.log_config import setup_logger

logger = setup_logger()


def download_model_local():
    """
    Download model from Hugging Face Hub to local directory.
    """
    # Путь к папке куда будем сохранять модель
    path_model = r"C:\DEV_python\teelgram_check_comments\model\cointegrated_rubert-tiny-sentiment-balanced"
    model = pipeline("text-classification", model="cointegrated/rubert-tiny-sentiment-balanced")
    model.model.save_pretrained(path_model)
    model.tokenizer.save_pretrained(path_model)


async def model_check_text(text):
    """
    get <- text
    return -> True, [{'label': 'toxic', 'score': 0.994674563407898}]
    """
    try:
        # путь к модели
        path_model = r"C:\DEV_python\teelgram_check_comments\model\cointegrated_rubert-tiny-sentiment-balanced"
        model = BertForSequenceClassification.from_pretrained(path_model)
        tokenizer = BertTokenizer.from_pretrained(path_model)
        nlp = pipeline("text-classification", model=model, tokenizer=tokenizer)
        # ответ модели
        sentiment = nlp(text)
        # Условие, score можно регулировать, пока не понятно, иногда видит негатив в простых словах
        if sentiment[0].get("score") > 0.75  and sentiment[0].get("label") == "negative":
            return True, sentiment
        return False, sentiment
    except Exception as e:
        logger.error(f"Error in model_check_text: {e}")
        return False, None


if __name__ == "__main__":
    result = asyncio.run(model_check_text("да что за хуйня"))
    print(result)
