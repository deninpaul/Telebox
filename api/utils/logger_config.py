import logging
import colorlog

logger = colorlog.getLogger()
logger.setLevel(logging.INFO)

formatter = colorlog.ColoredFormatter(
    "%(log_color)s[%(levelname)s] %(asctime)s: %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)