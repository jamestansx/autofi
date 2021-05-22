from subprocess import Popen, check_output

from modules.argcli import arg_cli
# from modules.config import getSettings
# setupselenium, wifiauth
from modules.settings.log import newLogging

# import sys



def isUtemWifi(wifiname="Kediaman_Pelajar"):
    alternatewifi = "Kediaman_Staff"
    if any(wifiname in check_wifiName() for wifiname in (wifiname, alternatewifi)):
        return True
    else:
        return False


def check_wifiName(status: bool = True):
    if status:
        return str(check_output("netsh wlan show interfaces"))
    else:
        connected_ssid = str(
            check_output(
                "powershell.exe (get-netconnectionProfile).Name", shell=True
            ).strip()
        )
        return connected_ssid.strip("b'")

'''
def setup(args):
    return getSettings()
    # ! Do not activate chrome driver as it will clog up the memory
    # ! as it doesn't close properly
    # webdriverPath, username, password, url, isFirstRun = config.getSettings()
    # if isFirstRun:
        # sys.exit(1)
    # try:
        # driver = setupselenium.setupSelenium(
        # webdriverPath, wifiauth.is_Connected(isDebug=args.isDebug), args.isDebug
        # )
        # return driver, username, password, url
    # except Exception:
        # return None, None, None, None
'''

def main():#driver, username, password, url, args):
    # setupselenium.open_webdriver(driver, url)
    # wifibot.bot(driver, username, password, args.isDebug)
    # FUCK I don't know about cURL and spending my time to do this bot
    # when in fact it can be done with this command
    return Popen('curl -s -d user="ogx" -d password="1234" "http://securelogin.arubanetworks.com/cgi-bin/login"')


if __name__ == "__main__":
    args = arg_cli()
    if isUtemWifi():
        # driver, username, password, url, isFirstRun = setup(args)
        main()
    else:
        logger = newLogging("log.log", isDebug=args.isDebug)
        connected_ssid = check_wifiName(isUtemWifi())
        logger.warning(f"Connected WiFi is {connected_ssid}...")
