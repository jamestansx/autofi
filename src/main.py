from modules import wifibot, wifiauth, setupselenium, config

import sys

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
