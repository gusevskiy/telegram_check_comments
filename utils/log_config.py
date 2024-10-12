import logging
from datetime import datetime

import colorlog


def setup_logger():
    log_colors = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }

    # Форматтер для цветных логов в консоли с нормальным временем
    console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - [%(levelname)s] - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
        log_colors=log_colors,
        datefmt='%Y-%m-%d %H:%M:%S'  # Формат времени
    )

    # Форматтер для логов в файле с нормальным временем
    file_formatter = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'  # Формат времени
    )

    # Настройка обработчика для консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    file_handler = logging.FileHandler(
        f"./logs/log_{datetime.now().strftime('%Y-%m-%d %H-%M')}.log"
    )
    file_handler.setFormatter(file_formatter)

    logging.basicConfig(level=logging.DEBUG, handlers=[console_handler, file_handler])

    logger = logging.getLogger(__name__)
    return logger
