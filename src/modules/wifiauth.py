from src.modules.settings import log
import urllib.request as request


def is_Connected(url="https://stackoverflow.com/", timeout=3):
    logger = log.newLogging("log.log")
    try:
        request.urlopen(url, timeout=timeout)
        logger.info("WiFi is connected and accessible.")
        return True
    except Exception as e:
        print(e)
        return False
