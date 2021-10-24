import os
import sys
from getpass import getpass

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from platform import system
from modules.argcli import arg_cli
from modules.settings.jsonfile import read_json, update_json, write_json
from modules.settings.setting import (
    change_password,
    delete_password,
    get_dirs,
    get_password,
    set_password,
)

appauthor = "jamestansx"
appname = "autofi"
userId = os.environ.get("USERNAME")


def isFirstRun(args=arg_cli()):
    userData_json = get_userdata_dir()
    response = None
    if os.path.isfile(userData_json):
        if args.isEdit and isEditSetting():
            editSetting(userData_json)
        return False
    else:
        setupSetting(userData_json)
        return True


def editSetting(userData_json):
    data = read_json(userData_json)
    console = Console()
    console.print(
        Panel(
            "1. Admin password (PC)\n2. task scheduler\n3. main executable path\n>>all",
            title="Select the setting to edit",
        )
    )
    choice = Prompt.ask(
        "[italic red]Choice", choices=["1", "2", "3", "all"], default="all"
    )
    if choice in {"1", "all"}:
        console.print(
            Panel(
                "1. [italic red]Change password\n[/]2. [italic red]Delete password",
                title="Password Setting",
                expand=False,
            )
        )
        response = Prompt.ask("[italic red]Choice", choices=["1", "2"])
        password_setting(response)
    if choice in {"2", "all"}:
        mainPath, password = getTaskInfo()
        create_task(mainPath, password)
    if choice in {"3", "all"}:
        console.print(
            Panel(
                f"(1) [bold red]Current Directory: [/][italic blue]{os.getcwd()}\n[/](2) [bold red]Specific Path",
                title="New Main Executable Path",
            )
        )
        inputChoice = Prompt.ask("[italic blue]Choice", choices=["1", "2"])
        isExePath(inputChoice)
    update_json(userData_json, data)


if system() == "Windows":
    from modules.settings import taskscheduler as scheduler
    def create_task(mainPath, password):
        isTaskScheduler = Confirm.ask("Do you want to setup task scheduler")
        if isTaskScheduler:
            scheduler.create_scheduler(mainPath, password)


def password_setting(response):
    if response in "1":
        change_password(appname, userId)
    if response in "2":
        delete_password(appname, userId)


def get_userdata_dir():
    dirs = get_dirs(appname, appauthor)
    return os.path.join(dirs["userData"], "userdata.json")


def isEditSetting():
    return Confirm.ask(
        "[bold red]Setting is already existed\n[/][bold italic white on red blink]Do you want to edit",
        default=True,
    )


def setupSetting(pathToFile):
    console = Console()
    console.rule("[bold blue]Task Scheduler Settings")
    console.print(
        Panel(
            f"(1) [bold red]Current Directory: [/][italic blue]{os.getcwd()}\n(2) [bold red]Specific Path",
            title="Main Executable Path",
        )
    )
    console.print()
    inputChoice = Prompt.ask("[italic blue]Choice", choices=["1", "2"])
    exePath = isExePath(inputChoice)
    adminPassword = getpass("Enter your admin password (PC): ")
    print()
    set_password(appname, userId, adminPassword)
    data = {"mainExecutablePath": exePath}
    write_json(pathToFile, writeSettings(data))


def isExePath(inputChoice):
    if inputChoice in "1":
        pwd = os.getcwd()
        name = appname + ".exe"
        for root, dirs, files in os.walk(pwd):
            if name in files:
                return os.path.join(root, name)
        else:
            Console().print("[bold red]autofi.exe is not found")
    return Prompt.ask("Enter the executable path")


def writeSettings(data):
    data["isFirstRun"] = False
    return data


def getTaskInfo():
    pathToFile = get_userdata_dir()
    if os.path.isfile(pathToFile):
        data = read_json(pathToFile)
        return data["mainExecutablePath"], get_password(appname, userId)
