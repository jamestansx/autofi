import logging
import os.path

from modules import config
from modules.settings import setting


def log(logger, level, filepath, isDebug=False):
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
    if isDebug:
        handler = logging.StreamHandler()
    else:
        handler = logging.FileHandler(filepath)
    handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(handler)


def newLogging(logFileName, logLevel="INFO", isDebug=False):
    logger = logging.getLogger()
    dirs = setting.get_dirs(config.appname, config.appauthor)
    logDir = os.path.join(dirs["userLog"], logFileName)
    if isDebug:
        level = logging.DEBUG
    else:
        choices = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARN": logging.WARN,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        level = choices.get(logLevel)
    log(logger, level, logDir, isDebug)
    return logger
