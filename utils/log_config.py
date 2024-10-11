import logging
import colorlog
from datetime import datetime

def setup_logger():
    log_colors = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - [%(levelname)s] - %(name)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
        log_colors=log_colors,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    handler = logging.FileHandler(f"./logs/log_{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.log")
    handler.setFormatter(formatter)

    logging.basicConfig(level=logging.INFO, handlers=[handler])

    logger = logging.getLogger(__name__)
    return logger
