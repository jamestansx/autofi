from subprocess import Popen, check_output

from modules.argcli import arg_cli
from modules.settings.log import newLogging



def isUtemWifi(wifiname="Kediaman_Pelajar"):
    alternatewifi = "Kediaman_Staff"
    return any(wifiname in check_wifiName() for wifiname in (wifiname, alternatewifi))


def check_wifiName(status: bool = True):
    if status:
        return str(check_output("netsh wlan show interfaces"))
    connected_ssid = str(
        check_output(
            "powershell.exe (get-netconnectionProfile).Name", shell=True
        ).strip()
    )
    return connected_ssid.strip("b'")



def main():
    # FUCK I don't know about cURL and spending my time to do this bot
    # when in fact it can be done with this command
    return Popen(
        'curl -s -d user="ogx" -d password="1234" "http://securelogin.arubanetworks.com/cgi-bin/login"'
    )


if __name__ == "__main__":
    args = arg_cli()
    if isUtemWifi():
        main()
    else:
        logger = newLogging("log.log", isDebug=args.isDebug)
        connected_ssid = check_wifiName(isUtemWifi())
        logger.warning(f"Connected WiFi is {connected_ssid}...")
