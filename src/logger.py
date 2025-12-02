import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logger(name="app", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)
    # Include only safe keys
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(request_id)s %(error)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
