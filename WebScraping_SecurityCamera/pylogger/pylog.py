import logging
from logging.handlers import TimedRotatingFileHandler
import sys
import os
FORMATTER = logging.Formatter("%(asctime)s: %(filename)s - %(levelname)s:%(funcName)s():%(lineno)d - %(message)s")
FORMATTER.datefmt = "%d-%b-%y %H:%M:%S"
LOG_FILE = "pylogger/app.log"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    if os.path.exists(LOG_FILE):    # When you re-run the app, the existing log must be removed
        os.remove(LOG_FILE)
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    file_handler.mode = 'a'   # append
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
    # Logging to both console and a file, if not needed just comment
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger
