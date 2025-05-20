import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def log_info(name, message):
    logger.info(f'{name}: {message}')

def log_error(name, message):
    logger.error(f'{name}: {message}')