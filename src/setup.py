from modules.config import isFirstRun, create_task, getTaskInfo

isFirstRun()
mainPath, password = getTaskInfo()
create_task(mainPath, password)
print("Setup is completed successfully")
