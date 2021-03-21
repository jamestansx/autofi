import urllib.request as request

from src.modules.settings import log


def is_Connected(url="https://stackoverflow.com/", timeout=3, isDebug = False):
    logger = log.newLogging("log.log", isDebug = isDebug)
    try:
        request.urlopen(url, timeout=timeout)
        logger.info("WiFi is connected and accessible.")
        return True
    except Exception as e:
        logger.info(f"Failed to connect - attempting to login - \n{e}")
        return False
