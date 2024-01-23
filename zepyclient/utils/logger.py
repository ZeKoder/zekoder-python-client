import logging
import inspect
from termcolor import colored
from pythonjsonlogger import jsonlogger
from .conf import get_config


class ColoredFormatter(logging.Formatter):
    COLORS = {"ERROR": "red", "WARNING": "yellow", "INFO": "green", "DEBUG": "blue"}

    def format(self, record):
        log_message = super().format(record)
        return colored(log_message, self.COLORS.get(record.levelname))


def get_logger(module_name: str = None):
    if not module_name:
        # Get the name of the module that called get_logger
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        module_name = module.__name__

    logger = logging.getLogger(module_name)
        
    if level_name:= get_config('DEBUG_LEVL'):
        level = logging.getLevelName(level_name.upper())
        logger.setLevel(level)  # Set the logging level
    else: 
        logger.setLevel(logging.DEBUG)
    # Check if running in GCP
    if get_config("CLOUD_HOSTED") == True:
        # Use JSON formatter for GCP
        # Including log level and module in the JSON output
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s"
        )
    else:
        # Use colored formatter for console
        formatter = ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - [%(lineno)d:%(funcName)s] - %(message)s"
        )

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger