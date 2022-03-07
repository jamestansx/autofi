import argparse
import getpass
import json
import logging
import os
import platform
import shutil
import subprocess
import sys

import yaml
from appdirs import AppDirs


def _init_log(dirs: AppDirs, logFile: str, args):
    logPath = os.path.join(dirs.user_log_dir, logFile)
    if not os.path.isfile(logPath):
        with open(logPath, 'x') as f:
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
        filename=logPath,
    )
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s: %(funcName)s:%(lineno)d %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )
    handler = (
        logging.StreamHandler() if args.debug else logging.FileHandler(logPath)
    )
    handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.debug("logging started")


def _init_args():
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
    return parser.parse_args()


def _init_yaml(yamlFile: str) -> dict:
    try:
        path = os.path.join(os.path.dirname(__file__), yamlFile) 
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        os.chdir(sys._MEIPASS)
        _init_yaml(yamlFile)

def _init_dirs(dirs:AppDirs):
    print(dirs.user_data_dir)
    print(dirs.user_log_dir)
    os.makedirs(dirs.user_data_dir, exist_ok=True)
    os.makedirs(dirs.user_log_dir, exist_ok=True)




def check_wifiname(wifilist):
    if platform.system() == "Windows":
        command = ["netsh", "wlan", "show", "interfaces"]
    else:
        command = ["iwgetid", "--raw"]
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    stdout, stderr = process.communicate()
    if stderr:
        print(f"Error occured: {stderr}")
        if "not found" in str(stderr):
            print("iwgetid is not installed. Please install 'iwgetid'")
            logging.error("iwgetid is not installed")
        logging.error("Cannot check wifi name")
        sys.exit(1)
    for wifi in wifilist:
        if wifi in stdout:
            break
    else:
        logging.debug("not found")
        return False
    return True


def create_config(filepath: str):
    data = dict(wifiname=list(), username=str(), password=str(), url=str())
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def edit_config(filepath: str):
    if not os.path.isfile(filepath):
        logging.debug("file not existed")
        create_config(filepath)
    if platform.system() == "Windows":
        os.startfile(filepath)
    else:
        subprocess.call(("vi", filepath))
    sys.exit(0)


def read_config(filepath: str) -> str:
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.debug("File not found...")
        logging.debug("Opening config file to write...")
        edit_config(filepath)
        sys.exit(1)


def cp_exe(infos, dirs):
    path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), infos["Filename"]["exe"])
    shutil.copy2(path, dirs.user_data_dir)
    return os.path.join(dirs.user_data_dir, infos["Filename"]["exe"])


def create_scheduler(infos, dirs):
    import win32com.client

    action_id = infos["appname"]
    action_path = cp_exe(infos, dirs)
    action_arguments = r""
    action_workdir = r""
    author = infos["appauthor"]
    description = infos["description"]
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


def main():
    yamlFile = "autofi.yaml"
    infos = _init_yaml(yamlFile)
    dirs = AppDirs(infos["appname"], infos["appauthor"])
    _init_dirs(dirs)
    args = _init_args()
    logFile = infos["Filename"]["log"]
    _init_log(dirs, logFile, args)
    configPath = os.path.join(dirs.user_data_dir, infos["Filename"]["config"])

    if platform.system() == "Windows":
        if args.addScheduler:
            create_scheduler(infos, dirs)

    if args.config:
        edit_config(configPath)

    data = read_config(configPath)
    if not all(i for i in data.values()):
        edit_config(configPath)

    if args.pconfig:
        print(json.dumps(data, indent=2))
        sys.exit(0)

    if check_wifiname(data["wifiname"]):
        output = os.popen(
            f"curl -sLI -d name='{data['username']}' -d password='{data['password']}' '{data['url']}' -w '%{{http_code}}' -o /dev/null",
        )
        output = output.read()
        logging.info(f"Wi-Fi connected: {output}")


if __name__ == "__main__":
    main()
