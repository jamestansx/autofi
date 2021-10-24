import re
from os import popen
from subprocess import PIPE, check_output
from platform import system
from sys import exit

from modules.argcli import arg_cli
from modules.settings.log import newLogging
from setup import setup

args=arg_cli()
logger = newLogging("log.log", isDebug=args.isDebug)

def isUtemWifi(wifiname="Kediaman_Pelajar"):
    alternatewifi = "Kediaman_Staff"
    if any(
        wifiname in check_wifiName(logger=logger) for wifiname in (wifiname, alternatewifi)
    ):
        return True
    else:
        connect_ssid = check_wifiName(False, logger=logger)
        logger.warning(f"Connected WiFi is {connected_ssid}...")
        return False


def check_wifiName(status: bool = True, logger=None):
    if system() == "Windows":
        command = "netsh wlan show interfaces"
    elif system() == "Linux":
        command = ["iwgetid", "--raw"]
    else:
        logger.error(f"{system()} is not supported")
        exit(-1)

    if status or system() == "Linux":
        return str(check_output(command))
    else:
        connected_ssid = str(
            check_output(
                "powershell.exe (get-netconnectionProfile).Name", shell=True
            ).strip()
        )
        return connected_ssid.strip("b'")


def main():
    if system() == "Windows" and setup():
        return False
    if isUtemWifi():
        output = popen(
            "curl -s -d user='ogx' -d password='1234' 'http://securelogin.arubanetworks.com/cgi-bin/login' -w '%{http_code}'", 
        )
        output = output.read()
        output = re.search("\d+$", output)
        logger.info(f"successfully connected:\n{output.group()}")
        exit(0)


if __name__ == "__main__":
    main()
