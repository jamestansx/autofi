import argparse
from dataclasses import dataclass
import json
import logging
import os
import platform
import re
import subprocess
import sys

from appdirs import AppDirs


CONFIGFILE = "config.json"
LOGFILE = "log.log"
EXEFILE= "autofi.exe"
APPAUTHOR = "jamestansx"
APPNAME = "autofi"
APPDIRS = AppDirs(APPNAME, APPAUTHOR)
DESCRIPTION = "Scheduler to autologin to Wi-Fi network login page"
VERSION = "2.0.0"

class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)

@dataclass
class Wifi_Profile:
    wifiname: str
    username: str
    password: str
    url: str

class Autofi(object):

    def __init__(self):
        self.configpath = os.path.join(APPDIRS.user_data_dir, CONFIGFILE)
        self.wifilist = self.scan_all_wifi()

    def add_config(self):
        while True:
            wifiname = input("Wifi SSID (input l to list all SSID): ")
            if wifiname == "l":
                for i in self.wifilist:
                    print(i)
                continue
            break
        username = input("Username : ")
        password = input("Password: ")
        url = input("Enter wifi login url: ")

        with open(self.configpath, 'w+') as f:
            data = f.read()
            profile = Wifi_Profile(wifiname, username, password, url)
            json.dump(data, f, indent=2, cls=EnhancedJSONEncoder)

    def read_config(self):
        try:
            with open(self.configpath, "r") as f:
                return json.load(f)
        #TODO: handle exception
        except FileNotFoundError:
            logging.warning("Config File does not exist...")
        except json.decoder.JSONDecodeError:
            logging.warning("Config File is empty")

    def print_config(self):
        print(json.dumps(self.read_config(), indent=2))

    def scan_all_wifi(self):
        results = subprocess.check_output(["netsh", "wlan", "show", "network"]).decode()
        results = results.replace("\r", "").split("\n")
        wifilist = list()
        for i in results:
            if "SSID" in i:
                #TODO: Find all better way to query SSID
                regex = re.compile(":.*$")
                wifilist.append(regex.findall(i).pop().replace(": ", ""))
        return wifilist

    def scan_wifi(self):
        if platform.system() == "Windows":
            command = ["netsh", "wlan", "show", "interfaces"]
        elif platform.system() == "Linux":
            logging.warning("NOT IMPLEMENTED")
            print("NOT IMPLEMENTED")
            sys.exit(2)
        else:
            logging.error("OS is not supported")
            sys.exit(1)
        
        stdout = subprocess.check_output(command).decode()
        print("stdout", stdout)
        for wifi in self.wifilist:
            if wifi in stdout:
                return wifi 
        logging.debug("No wifi is matched")
        return None

    def login(self):
        data = self.read_config()
        wifi = self.scan_wifi()
        if wifi is not None:
            output = os.popen(
                    f"curl -sL -d user='{wifi}' -d password='{data[wifi]['password']}' '{data[wifi]['url']}' -w '%{{http_code}}'",
                    )
            output = output.read()
            logging.debug(f"HTTP CODE: {output}")


def initlog(args):

    logpath = os.path.join(APPDIRS.user_log_dir, LOGFILE)
    if not os.path.isfile(logpath):
        with open(logpath, 'x') as f:
            ...

    if args.debug:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logger = logging.getLogger()
    logging.basicConfig(
        filemode="a",
        format="%(asctime)s %(levelname)s: %(funcName)s:%(lineno)d %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        filename=logpath,
    )
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s: %(funcName)s:%(lineno)d %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )
    handler = (
        logging.StreamHandler() if args.debug else logging.FileHandler(logpath)
    )
    handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.debug("logging started")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        "-c",
        default=False,
        action="store_true",
        help="Open config file to edit configuration",
    )
    parser.add_argument(
        "--pconfig",
        "-p",
        default=False,
        action="store_true",
        help="Get configuration and print them",
    )
    parser.add_argument(
        "--debug",
        "-d",
        default=False,
        action="store_true",
        help="Enable debug mode",
    )
    if platform.system() == "Windows":
        parser.add_argument(
            "--add-scheduler",
            "-as",
            default=False,
            dest="addScheduler",
            action="store_true",
            help="Add Windows task scheduler",
        )
    args = parser.parse_args()
    initlog(args)
    os.makedirs(APPDIRS.user_data_dir, exist_ok=True)
    os.makedirs(APPDIRS.user_log_dir, exist_ok=True)
    autofi = Autofi()
    if args.config:
        autofi.add_config()
        sys.exit(0)

    if args.pconfig:
        autofi.print_config()
        sys.exit(0)

    autofi.login()
