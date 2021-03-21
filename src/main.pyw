import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.modules import config, setupselenium, wifiauth, wifibot, argcli


def setup(args):
    webdriverPath, username, password, url, isFirstRun = config.getSettings()
    if isFirstRun:
        sys.exit(1)

    driver = setupselenium.setupSelenium(
        webdriverPath, wifiauth.is_Connected(isDebug=args.isDebug), args.isDebug
    )
    return driver, username, password, url


def main(driver, username, password, url, args):
    setupselenium.open_webdriver(driver, url)
    wifibot.bot(driver, username, password, args.isDebug)


if __name__ == "__main__":
    args = argcli.arg_cli()
    driver, username, password, url = setup(args)
    main(driver, username, password, url)
