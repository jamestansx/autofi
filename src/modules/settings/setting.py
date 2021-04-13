import os
from getpass import getpass

import keyring
from appdirs import AppDirs


def get_dirs(appname, appauthor, dirs={}):
    dir = AppDirs(appname, appauthor)
    dirs["userData"] = dir.user_data_dir
    dirs["userLog"] = dir.user_log_dir
    make_dir(dirs)
    return dirs


def make_dir(dirs):
    for dir in dirs:
        try:
            os.makedirs(dirs[dir], exist_ok=True)
        except OSError:
            pass
    return True


def set_password(appname, username, password):
    keyring.set_password(appname, username, password)


def change_password(appname, username):
    new_password = getpass("Enter your new password: ")
    keyring.set_password(appname, username, new_password)


def delete_password(appname, username):
    keyring.delete_password(appname, username)


def get_password(appname, username):
    return keyring.get_password(appname, username)
