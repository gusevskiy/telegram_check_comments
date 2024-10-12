import logging
from datetime import datetime
import sys
import os


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Логирование в файл с кодировкой UTF-8
    file_handler  = logging.FileHandler(f"./logs/log_{datetime.now().strftime('%Y-%m-%d')}.log", encoding='utf-8')
    file_handler .setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    # Формат сообщений лога
    formatter = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S' 
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    
    return logger
