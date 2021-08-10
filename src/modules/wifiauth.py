import urllib.request as request

from modules.settings import log


def is_Connected(url="https://stackoverflow.com/", timeout=5, isDebug=False):
    logger = log.newLogging("log.log", isDebug=isDebug)
    attempts = 0
    while True & attempts < 3:
        try:
            attempts += 1
            request.urlopen(url, timeout=timeout)
            logger.info("WiFi is connected and accessible.")
            return True
        except Exception as e:
            if attempts == 2:
                logger.error("Last trial==>Too many trial!!")
            if str(e) in "urlopen error [Errno 11001] getaddrinfo failed":
                logger.warn(
                    f"Failed to open url - attempting to reopen - \n{e}\n"
                )
                continue
            else:
                logger.info(
                    f"WiFi is not authenticated -- attempting to authenticate -- \n{e}\n"
                )
                return False
