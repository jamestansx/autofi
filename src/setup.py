from modules.config import isFirstRun, create_task, getTaskInfo

def setup():
    if isFirstRun():
        mainPath, password = getTaskInfo()
        create_task(mainPath, password)
        print("Setup is completed successfully")
        return True
    else:
        return False

