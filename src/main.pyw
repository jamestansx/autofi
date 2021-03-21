import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.modules import config, setupselenium, wifiauth, wifibot


def setup():
    webdriverPath, username, password, url, isFirstRun = config.getSettings()
    if isFirstRun:
        sys.exit(1)

    driver = setupselenium.setupSelenium(webdriverPath, wifiauth.is_Connected())
    return driver, username, password, url

def main(driver, username, password, url):
    setupselenium.open_webdriver(driver, url)
    wifibot.bot(driver, username, password)

if __name__ == "__main__":
    driver, username, password, url = setup()
    main(driver, username, password, url)
