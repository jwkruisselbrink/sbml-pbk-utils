import logging
import uuid

def create_console_logger() -> logging.Logger:
    # Configure logger for formatted console output
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

def create_file_logger(logfile: str) -> logging.Logger:
    logger = logging.getLogger(uuid.uuid4().hex)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logfile, 'w+')
    formatter = logging.Formatter('[%(levelname)s] - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
