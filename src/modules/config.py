import sys, os
from src.modules.settings import setting
from src.modules.settings import jsonfile

appauthor = "jamestansx"
appname = "auth_Wifi_UTeM"


def isFirstRun():
    userData_json = get_userdata_dir()
    response = None
    if os.path.isfile(userData_json):
        response = isEditSetting()
    else:
        setupSetting(userData_json)

    if response:
        editSetting(userData_json)
    else:
        sys.exit()


def editSetting(userData_json):
    data = jsonfile.read_json(userData_json)
    choice = input(
        "Select the setting to edit:\n1. chrome driver path\n2. username\n3. password\n4. url\n[all]\n"
    )
    if choice in {"1", "all"}:
        data["webdriverPath"] = input("Chrome driver path: ")
    if choice in {"2", "3", "all"}:
        data["username"] = input("Username: ")
    if choice in {"3", "all"}:
        response = input("---------------\n1. Change password\n2. Delete password\n")
        password_setting(data, response)
    if choice in {"4", "all"}:
        data["url"] = input("New url: ")
    jsonfile.update_json(userData_json, data)


def password_setting(data, response):
    if response in "1":
        setting.change_password(appname, data["username"])
    if response in "2":
        setting.delete_password(appname, data["username"])


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
    webdriverPath = input("Enter the path to Chrome driver: ")
    url = input("Enter the URL: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    setting.set_password(appname, username, password)
    data = {"webdriverPath": webdriverPath, "username": username, "url": url}
    jsonfile.write_json(pathToFile, writeSettings(data))


def writeSettings(data):
    data["isFirstRun"] = False
    return data


def getSettings():
    pathToFile = get_userdata_dir()
    if os.path.isfile(pathToFile):
        data = jsonfile.read_json(pathToFile)
        return (
            data["webdriverPath"],
            data["username"],
            setting.get_password(appname, data["username"]),
            data["url"],
            data["isFirstRun"],
        )
    return None, None, None, None, True
