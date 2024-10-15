import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import asyncio
from pathlib import Path

from transformers import BertForSequenceClassification, BertTokenizer, pipeline

from utils.log_config import setup_logger

logger = setup_logger()


def download_model_local():
    """
    Download model from Hugging Face Hub to local directory.
    """
    try:
        # Путь к папке куда будем сохранять модель (Модель ставится только по абсолютному пути)
        path_model = Path("telegram_check_comments").parent.absolute()  / "model" / "cointegrated_rubert-tiny-sentiment-balanced"
        path_model.mkdir(parents=True, exist_ok=True)
        logger.info(f"папка для модели создана {path_model}")
        if Path(path_model).exists():
            model = pipeline(
                "text-classification", model="cointegrated/rubert-tiny-sentiment-balanced"
            )
            model.model.save_pretrained(path_model.absolute())
            model.tokenizer.save_pretrained(path_model.absolute())
            logger.info("Модель успешно загружена и сохранена")
    except Exception as e:
        logger.error(f"Error in download_model_local: {e}")


async def model_check_text(text):
    """
    get <- text
    return -> True, [{'label': 'negative', 'score': 0.994674563407898}]
    """
    try:
        # путь к модели
        path_model = r"\model\cointegrated_rubert-tiny-sentiment-balanced"
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
    try:
        download_model_local()
        # ждем чтоб модель загрузилась
        time.sleep(3)
        # код для проверки работы модели
        result, sentiment = asyncio.run(model_check_text('Да что за хрень тут творится'))
        logger.info(f"{result} -> {sentiment}")
    except Exception as e:
        logger.error(f"Error in main: {e}")
