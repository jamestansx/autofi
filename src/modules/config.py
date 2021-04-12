from getpass import getpass
import os
import sys

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
    choice = input(
        "Select the setting to edit:\n1. chrome driver path\n2. username\n3. password\n4. url\n5. task scheduler\n6. main executable path\n[all]\n"
    )
    if choice in {"1", "all"}:
        data["webdriverPath"] = input("Chrome driver path: ")
    if choice in {"2", "all"}:
        data["username"] = input("Username: ")
    if choice in {"3", "all"}:
        response = input("---------------\n1. Change password\n2. Delete password\n")
        password_setting(data, response)
    if choice in {"4", "all"}:
        data["url"] = input("New url: ")
    if choice in {"5", "all"}:
        mainPath, password = getSettings(True)
        create_task(mainPath, password)
    if choice in {"6", "all"}:
        inputChoice = input("new main executable path: \n(1) Default (Current Path)\n(2) Specify path\n")
        isExePath(inputChoice)
    jsonfile.update_json(userData_json, data)

def create_task(mainPath, password):
    isTaskScheduler = input("Do you want to setup task scheduler (y/n): ")
    if isTaskScheduler in {"y", "yes"}:
        scheduler.create_scheduler(mainPath, password)

def password_setting(data, response):
    if response in "1":
        whichPassword = input("Which password to change: \n(1) Wifi User Credential\n(2) User Admin\n")
        if whichPassword in "1":
            setting.change_password(appname, data["username"])
        elif whichPassword in "2":
            setting.change_password(appname, userId)
    if response in "2":
        whichPassword = input("Which password to change: \n(1) Wifi User Credential\n(2) User Admin\n")
        if whichPassword in "1":
            setting.delete_password(appname, data["username"])
        elif whichPassword in "2":
            setting.delete_password(appname, userId)

def get_userdata_dir():
    dirs = setting.get_dirs(appname, appauthor)
    userData_json = os.path.join(dirs["userData"], "userdata.json")
    return userData_json


def isEditSetting():
    while True:
        response = input("Setting is already existed\nDo you want to edit <y/n>: ")
        if response.strip().lower() in {"y", "yes"}:
            return True
        elif response.strip().lower() in {"n", "no"}:
            return False
        else:
            pass


def setupSetting(pathToFile):
    print("General Setup\n----------------------------------------------------------------\n")
    webdriverPath = input("Enter the path to Chrome driver: ")
    url = input("Enter the URL: ")
    print("WiFi credentials settings\n----------------------------------------------------------------\n")
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")
    setting.set_password(appname, username, password)
    print("Task Scheduler Settings\n----------------------------------------------------------------\n")
    inputChoice = input("main executable path: \n(1) Default (Current Path)\n(2) Specify path\n")
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
            return input("Enter the executable path: ")
        else:
            inputChoice = input("Please select the appropriate choice (1/2): ")

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
