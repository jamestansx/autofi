import logging
import os.path

from src.modules import config
from src.modules.settings import setting


def log(logger, level, filepath):
    logging.basicConfig(
        filemode="a",
        format="%(asctime)s %(levelname)s: %(funcName)s:%(lineno)d %(message)s",
        encoding="utf-8",
        datefmt="%d-%b-%y %H:%M:%S",
        filename=filepath,
    )
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s: %(funcName)s:%(lineno)d %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )
    handler = logging.FileHandler(filepath)
    handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(handler)

def newLogging(logFileName, logLevel = "INFO"):
    logger = logging.getLogger()
    dirs = setting.get_dirs(config.appname, config.appauthor)
    logDir = os.path.join(dirs["userLog"], logFileName)
    choices = {"DEBUG":logging.DEBUG, "INFO": logging.INFO, "WARN": logging.WARN, "ERROR": logging.ERROR, "CRITICAL": logging.CRITICAL}
    level = choices.get(logLevel, logging.INFO)
    log(logger, level, logDir)
    return logger
