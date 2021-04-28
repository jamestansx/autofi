import os

import win32com.client


def create_scheduler(executable_path, userPassword):
    # Uses the COM Task Scheduler Interface to create a task
    # scheduled to execute when the current user logs on.

    action_id = "autofi-utem"  # arbitrary action ID
    action_path = rf"{executable_path}"  # executable path (could be python.exe)
    action_arguments = r""  # arguments (could be something.py)
    action_workdir = r""  # working directory for action executable
    author = "jamestansx"  # so that end users know who you are
    description = "Automatically authenticate login to connect to UTeM WiFi"
    task_id = action_id
    task_hidden = False  # set this to True to hide the task in the interface

    # define constants
    TASK_TRIGGER_EVENT = 0
    TASK_ACTION_EXEC = 0
    TASK_LOGON_PASSWORD = 1
    TASK_CREATE_OR_UPDATE = 6
    TASK_TRIGGER_LOGON = 9

    # connect to the scheduler (Vista/Server 2008 and above only)
    scheduler = win32com.client.Dispatch("Schedule.Service")
    scheduler.Connect()
    rootFolder = scheduler.GetFolder("\\")

    # (re)define the task
    taskDef = scheduler.NewTask(0)
    taskDef.Settings.DisallowStartIfOnBatteries = False
    colTriggers = taskDef.Triggers

    trigger = colTriggers.Create(TASK_TRIGGER_LOGON)
    trigger.Id = "LogonTriggerId"
    trigger.UserId = os.environ.get("USERNAME")  # current user account

    trigger2 = colTriggers.Create(TASK_TRIGGER_EVENT)
    trigger2.Subscription = """<QueryList>
  <Query Id="0" Path="Microsoft-Windows-WLAN-AutoConfig/Operational">
    <Select Path="Microsoft-Windows-WLAN-AutoConfig/Operational">*[System[(EventID=8000)]]</Select>
  </Query>
</QueryList>"""

    trigger3 = colTriggers.Create(TASK_TRIGGER_EVENT)
    trigger3.Subscription = """<QueryList>
  <Query Id="0" Path="System">
    <Select Path="System">*[System[Provider[@Name='Microsoft-Windows-Power-Troubleshooter'] and (EventID=1)]]</Select>
  </Query>
</QueryList>"""

    colActions = taskDef.Actions
    action = colActions.Create(TASK_ACTION_EXEC)
    action.ID = action_id
    action.Path = action_path
    action.WorkingDirectory = action_workdir  # StartIn
    action.Arguments = action_arguments

    info = taskDef.RegistrationInfo
    info.Author = author
    info.Description = description

    settings = taskDef.Settings
    # settings.Enabled = False
    settings.Hidden = task_hidden
    # settings.StartWhenAvailable = True

    # register the task (create or update, just keep the task name the same)
    rootFolder.RegisterTaskDefinition(
        task_id, taskDef, TASK_CREATE_OR_UPDATE, trigger.UserId, userPassword, TASK_LOGON_PASSWORD
    )


create_scheduler("D:\Project Work\Programming project\Python\AutoWifiAuth\src\dist\main.exe", "Str@ng3Quark_1021")
