from modules import config

config.isFirstRun()
mainPath, password = config.getTaskInfo()
config.create_task(mainPath, password)
print("Setup is completed successfully")
