from getpass import getpass
import os
import sys
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.prompt import Confirm
from modules.settings import jsonfile, setting
from modules.settings import taskscheduler as scheduler

appauthor = "jamestansx"
appname = "auth_Wifi_UTeM"
userId = os.environ.get("USERNAME")

def isFirstRun():
    userData_json = get_userdata_dir()
    response = None
    if os.path.isfile(userData_json):
        response = isEditSetting()
        if response:
            editSetting(userData_json)
        sys.exit()
    else:
        setupSetting(userData_json)



def editSetting(userData_json):
    data = jsonfile.read_json(userData_json)
    console = Console()
    console.print(Panel("1. chrome driver path\n2. username\n3. password\n4. url\n5. task scheduler\n6. main executable path\n>>all", title="Select the setting to edit"))
    choice = Prompt.ask("[italic red]Choice", choices=["1", "2", "3", "4", "5", "6", "all"], default="all")
    if choice in {"1", "all"}:
        data["webdriverPath"] = Prompt.ask("[italic green]Chrome driver path")
    if choice in {"2", "all"}:
        data["username"] = Prompt.ask("[italic green]Username")
    if choice in {"3", "all"}:
        console.print(Panel("1. [italic red]Change password\n[/]2. [italic red]Delete password", title="Password Setting", expand=False))
        response = Prompt.ask("[italic red]Choice", choices=["1", "2"])
        password_setting(data, response, console)
    if choice in {"4", "all"}:
        data["url"] = Prompt.ask("[italic green]New url")
    if choice in {"5", "all"}:
        mainPath, password = getSettings(True)
        create_task(mainPath, password)
    if choice in {"6", "all"}:
        console.print(Panel(f"(1) [bold red]Current Directory: [/][italic blue]{os.getcwd()}\n[/](2) [bold red]Specific Path", title="New Main Executable Path", ))
        inputChoice = Prompt.ask("[italic blue]Choice", choices=["1", "2"])
        isExePath(inputChoice)
    jsonfile.update_json(userData_json, data)

def create_task(mainPath, password):
    isTaskScheduler = Confirm.ask("Do you want to setup task scheduler")
    if isTaskScheduler in {"y", "yes"}:
        scheduler.create_scheduler(mainPath, password)

def password_setting(data, response, console):
    if response in "1":
        console.print(Panel("(1) [italic blue]Wifi User Credential\n[/](2) [italic blue]User Admin\n", title="Which password to change"))
        whichPassword = Prompt.ask("[italic blue]Choice", choices=["1", "2"])
        if whichPassword in "1":
            setting.change_password(appname, data["username"])
        elif whichPassword in "2":
            setting.change_password(appname, userId)
    if response in "2":
        console.print(Panel("(1) [italic blue]Wifi User Credential\n(2) [italic blue]User Admin\n", title="Which password to delete"))
        whichPassword = Prompt.ask("[italic blue]Choice", choices=["1", "2"])
        if whichPassword in "1":
            setting.delete_password(appname, data["username"])
        elif whichPassword in "2":
            setting.delete_password(appname, userId)

def get_userdata_dir():
    dirs = setting.get_dirs(appname, appauthor)
    userData_json = os.path.join(dirs["userData"], "userdata.json")
    return userData_json


def isEditSetting():
    return Confirm.ask("[bold red]Setting is already existed\n[/][bold italic white on red blink]Do you want to edit", default=True)

def setupSetting(pathToFile):
    console = Console()
    console.rule("[bold red]General Setup")
    webdriverPath = Prompt.ask("[italic red]Enter the path to Chrome driver")
    url = Prompt.ask("[italic red]Enter the URL")
    console.rule("[bold purple]WiFi credentials settings")
    username = Prompt.ask("[italic purple]Enter your username")
    password = Prompt.ask("[italic purple]Enter your password", password=True)
    setting.set_password(appname, username, password)
    console.rule("[bold blue]Task Scheduler Settings")
    console.print(Panel(f"(1) [bold red]Current Directory: [/][italic blue]{os.getcwd()}\n(2) [bold red]Specific Path", title="Main Executable Path"))
    console.print()
    inputChoice = Prompt.ask("[italic blue]Choice", choices=["1", "2"])
    exePath = isExePath(inputChoice)
    adminPassword = getpass("Enter your admin password: ")
    setting.set_password(appname, userId, adminPassword)
    data = {"webdriverPath": webdriverPath, "username": username, "url": url, "mainExecutablePath": exePath}
    jsonfile.write_json(pathToFile, writeSettings(data))

def isExePath(inputChoice):
    while True:
        if inputChoice in "1":
            pwd = os.getcwd()
            name = "main.exe"
            for root, dirs, files in os.walk(pwd):
                if name in files:
                    return os.path.join(root, name)
        elif inputChoice in "2":
            return Prompt.ask("Enter the executable path")

def writeSettings(data):
    data["isFirstRun"] = False
    return data


def getSettings(isSetup=False):
    pathToFile = get_userdata_dir()
    if os.path.isfile(pathToFile):
        data = jsonfile.read_json(pathToFile)
        if isSetup:
            return data["mainExecutablePath"], setting.get_password(appname, userId)
        return (
            data["webdriverPath"],
            data["username"],
            setting.get_password(appname, data["username"]),
            data["url"],
            data["isFirstRun"],
        )
    return None, None, None, None, True
