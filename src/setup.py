from platform import system
from modules.config import isFirstRun
def setup():
    if isFirstRun():
        if system() == "Windows":
            from modules.config import create_task, getTaskInfo
            mainPath, password = getTaskInfo()
            create_task(mainPath, password)
        print("Setup is completed successfully")
        return True
    else:
        return False

