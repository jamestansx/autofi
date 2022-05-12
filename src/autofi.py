import argparse
import getpass
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

        try:
            with open(self.configpath, 'r') as f:
                data = f.read()
                logging.debug(f"Config: {data}")
        except FileNotFoundError:
            data = None

        with open(self.configpath, 'w') as f:
            profile = { "username": username, "password": password, "url": url }
            if data is None:
                data = { wifiname: profile }
            else:
                data = json.loads(data)
                data[wifiname] = profile
            logging.debug(f"Config: {data}")
            json.dump(data, f, indent=2,)
            logging.info("Configuration is added")

    def update_config(self):
        data = self.read_config()
        for i,n in enumerate(data.keys()):
            print(f"{i}) {n}")
        choice = input("Enter the index of profile to be updated: ")
        profile = list(data)[int(choice)]
        print(f"Updating {profile}...")
        username = input("Username : ")
        password = input("Password: ")
        url = input("Enter wifi login url: ")
        update = dict(username=username, password=password, url=url)
        data[profile] = update
        logging.debug(f"Config: {data}")
        with open(self.configpath, 'w') as f:
            json.dump(data, f, indent=2)
            logging.info("Configuration is updated")

    def read_config(self):
        try:
            with open(self.configpath, "r") as f:
                return json.load(f)
        #TODO: handle exception
        except FileNotFoundError:
            logging.warning("Config File does not exist...")
        except json.decoder.JSONDecodeError:
            logging.warning("Config File is empty")
        return None

    def print_config(self):
        print(json.dumps(self.read_config(), indent=2))

    def scan_all_wifi(self):
        if platform.system() == "Windows":
            command = ["netsh", "wlan", "show", "network"]
            logging.debug("Windows OS is detected")
        elif platform.system() == "Linux":
            logging.warning("Linux is detected")
            print("NOT IMPLEMENTED")
            sys.exit(2)
        else:
            logging.error(f"{platform.system()} OS is not supported")
            print(f"{platform.system()} OS is not supported")
            sys.exit(1)

        results = subprocess.getoutput(command)
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
        for wifi in self.wifilist:
            if wifi in stdout:
                logging.info(f"{wifi} is found")
                return wifi 
        logging.debug("Wifi is not matched")
        return None

    def login(self):
        data = self.read_config()
        if data is None:
            logging.warning("No configuration is found...")
            self.add_config()
            data = self.read_config()
        wifi = self.scan_wifi()
        if wifi is not None:
            curl = f'curl -d user="{data[wifi]["username"]}" -d password="{data[wifi]["password"]}" {data[wifi]["url"]} -w "%{{http_code}}" -o NUL'
            #curl = f"curl -d user='{data[wifi]['username']}' -d password='{data[wifi]['password']}' {data[wifi]['url']}"
            logging.debug(f"command: {curl}")
            output = os.popen(curl)
            output = output.read()
            logging.info("Login successfully")
            logging.debug(f"HTTP CODE: {output}")

    def create_scheduler(self):
        self.addenv()
        import win32com.client

        action_id = APPNAME
        action_path = self.copyexe()
        action_arguments = r""
        action_workdir = r""
        author = APPAUTHOR
        description = DESCRIPTION
        task_id = action_id
        task_hidden = False
        userdomain = os.environ.get("USERDOMAIN")
        username = os.environ.get("USERNAME")
        userPassword = getpass.getpass(
            prompt=f"Enter your user password ({username})"
        )

        TASK_TRIGGER_EVENT = 0
        TASK_ACTION_EXEC = 0
        TASK_LOGON_PASSWORD = 1
        TASK_CREATE_OR_UPDATE = 6
        TASK_TRIGGER_LOGON = 9

        try:
            scheduler = win32com.client.Dispatch("Schedule.Service")
            scheduler.Connect()
            rootFolder = scheduler.GetFolder("\\")

            taskDef = scheduler.NewTask(0)
            taskDef.Settings.DisallowStartIfOnBatteries = False
            colTriggers = taskDef.Triggers

            trigger = colTriggers.Create(TASK_TRIGGER_LOGON)
            trigger.Id = "LogonTriggerId"
            trigger.UserId = userdomain + "\\" + username

            trigger2 = colTriggers.Create(TASK_TRIGGER_EVENT)
            trigger2.Subscription = """<QueryList>
          <Query Id="0" Path="Microsoft-Windows-WLAN-AutoConfig/Operational">
            <Select Path="Microsoft-Windows-WLAN-AutoConfig/Operational">*[System[(EventID=8000)]]</Select>
          </Query>
        </QueryList>"""

            trigger3 = colTriggers.Create(TASK_TRIGGER_EVENT)
            trigger3.Subscription = """<QueryList>
          <Query Id="0" Path="System">
            <Select Path="System">*[System[Provider[@Name='Microsoft-Windows-Power-Troubleshooter'] and (EventID=1)]]</Select>
          </Query>
        </QueryList>"""

            colActions = taskDef.Actions
            action = colActions.Create(TASK_ACTION_EXEC)
            action.ID = action_id
            action.Path = action_path
            action.WorkingDirectory = action_workdir
            action.Arguments = action_arguments

            info = taskDef.RegistrationInfo
            info.Author = author
            info.Description = description

            settings = taskDef.Settings
            settings.Hidden = task_hidden

            rootFolder.RegisterTaskDefinition(
                task_id,
                taskDef,
                TASK_CREATE_OR_UPDATE,
                trigger.UserId,
                userPassword,
                TASK_LOGON_PASSWORD,
            )
            logging.info("Scheduler is created")
        except Exception as e:
            logging.error("Scheduler creation failed: e")

    def copyexe(self):
        import shutil
        path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), EXEFILE)
        shutil.copy2(path, APPDIRS.user_data_dir)
        logging.info(f"{EXEFILE} is copied")
        return os.path.join(APPDIRS.user_data_dir, EXEFILE)

    def addenv(self):
        path = APPDIRS.user_data_dir
        command = f"$env:Path+={path};[Environment]::SetEnvironmentVariable('AUTOFI', $env:Path, 'Machine')"
        out = subprocess.run(["powershell", "-Command", command], capture_output=True)
        if out.returncode != 0:
            print(f"Error occur: {out.stderr}")
            print("--------------------------")
            print("Please run in admin shell")


def initargs():
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
        "--update",
        "-u",
        default=False,
        action="store_true",
        help="Update profile configuration",
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
    return parser.parse_args()


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


def pathsetup():
    os.makedirs(APPDIRS.user_data_dir, exist_ok=True)
    os.makedirs(APPDIRS.user_log_dir, exist_ok=True)


def setup():
    pathsetup()
    args = initargs()
    initlog(args)
    return args


if __name__ == "__main__":
    args = setup()
    autofi = Autofi()

    if args.config:
        autofi.add_config()
        sys.exit(0)

    if args.pconfig:
        autofi.print_config()
        sys.exit(0)
    if args.update:
        autofi.update_config()
        sys.exit(0)

    if args.addScheduler and platform.system() == "Windows":
        autofi.create_scheduler()
        sys.exit(0)

    autofi.login()
