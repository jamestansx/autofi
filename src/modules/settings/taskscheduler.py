from os import environ

import win32com.client


def create_scheduler(executable_path, userPassword):

    action_id = "autofi-utem"
    action_path = rf"{executable_path}"
    action_arguments = r""
    action_workdir = r""
    author = "jamestansx"
    description = "Automatically authenticate login to connect to UTeM WiFi"
    task_id = action_id
    task_hidden = False

    TASK_TRIGGER_EVENT = 0
    TASK_ACTION_EXEC = 0
    TASK_LOGON_PASSWORD = 1
    TASK_CREATE_OR_UPDATE = 6
    TASK_TRIGGER_LOGON = 9

    scheduler = win32com.client.Dispatch("Schedule.Service")
    scheduler.Connect()
    rootFolder = scheduler.GetFolder("\\")

    taskDef = scheduler.NewTask(0)
    taskDef.Settings.DisallowStartIfOnBatteries = False
    colTriggers = taskDef.Triggers

    trigger = colTriggers.Create(TASK_TRIGGER_LOGON)
    trigger.Id = "LogonTriggerId"
    trigger.UserId = environ.get("USERDOMAIN") + "\\" + environ.get("USERNAME")

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
    action.WorkingDirectory = action_workdir
    action.Arguments = action_arguments

    info = taskDef.RegistrationInfo
    info.Author = author
    info.Description = description

    settings = taskDef.Settings
    settings.Hidden = task_hidden

    rootFolder.RegisterTaskDefinition(
        task_id,
        taskDef,
        TASK_CREATE_OR_UPDATE,
        trigger.UserId,
        userPassword,
        TASK_LOGON_PASSWORD,
    )
