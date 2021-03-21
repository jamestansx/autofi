import os, sys, subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.modules import config, setupselenium, wifiauth, wifibot, argcli
from src.modules.settings import log

def isUtemWifi(wifiname="Kediaman_Pelajar"):
    if wifiname in check_wifiName():
        return True
    else:
        return False

def check_wifiName(status:bool=True):
    if status:
        return str(subprocess.check_output("netsh wlan show interfaces"))
    else:
        connected_ssid = str(subprocess.check_output("powershell.exe (get-netconnectionProfile).Name", shell=True).strip())
        return connected_ssid.strip("b'")

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
    if isUtemWifi():
        driver, username, password, url = setup(args)
        main(driver, username, password, url, args)
    else:
        logger = log.newLogging("log.log", isDebug = args.isDebug)
        connected_ssid = check_wifiName(isUtemWifi())
        logger.warning(f"Connected WiFi is {connected_ssid}...")
