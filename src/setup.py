from modules import config

config.isFirstRun()
mainPath, password = config.getSettings(True)
config.create_task(mainPath, password)
print("Setup is completed successfully")
