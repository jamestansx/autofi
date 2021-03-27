<h1 align="center">autofi-utem</h1>
<h4 align="center">An automation to authenticate login process to UTeM Kediaman_Pelajar WiFi</h4>
<div align="center">
  <img alt="GitHub" src="https://img.shields.io/github/license/jamestansx/autofi-utem?logo=lgtm&logoWidth=18&color=bright%20green">
  <img alt="LGTM Grade" src="https://img.shields.io/lgtm/grade/python/github/jamestansx/autofi-utem?logo=lgtm&logoWidth=18">
  <a href="https://lgtm.com/projects/g/jamestansx/autofi-utem/alerts/"><img alt="Total alerts" src="https://img.shields.io/lgtm/alerts/g/jamestansx/autofi-utem.svg?logo=lgtm&logoWidth=18"/></a>
</div>

---

# Installation

Prerequisite:

- python version > 3.6.x
- libraries in [requirements.txt](https://github.com/jamestansx/autofi-utem/blob/07778903a6ed82405ba2151f465bdf723a5970d1/requirements.txt)
  ```markdown
  $ pip install -r requirements.txt
  ```
- [Chrome driver](https://chromedriver.chromium.org/downloads)

Clone this repo:

- Git

  ```markdown
  $ git clone https://github.com/jamestansx/autofi-utem.git
  ```

- GitHub CLI
  ```markdown
  $ gh repo clone jamestansx/autofi-utem
  ```

---

# Setup configuration

1. navigate to the directory the repo is cloned into (if you haven't do so)
   ```markdown
   $ cd path/to/repo
   ```
2. Run the setup.py
   ```markdown
   $ python setup.py
   ```
3. Configure the required information

   ```markdown
   - Chrome driver's path
   - Username
   - Password
   - Url to login page
   ```

   \*Note: The url can be obtained from the browser's history

4. (Optional) To update the configuration, repeat the same process.

---

# Usage

<h4>Warning: The Schedular is not working stablely (sometimes).</h4>
There are two options to run this script:

1. _**Terminal**_

   Run this code to activate the [script](https://github.com/jamestansx/autofi-utem/blob/07778903a6ed82405ba2151f465bdf723a5970d1/src/main.py)

   ```markdown
   $ python path/to/main.py
   ```

   Optional arguments to pass in:

   ```markdown
   usage: AutoFi-UTeM [-h] [--debug]

   A bot to automatically authenticate UTeM WiFi

   optional arguments:
   -h, --help show this help message and exit
   -d, --debug Enable debug mode
   ```

2. _**Scheduler Setup**_

- _Windows_

  Multiple Triggers:

  1. On an event
     1. Log
        ```markdown
        Microsoft-Windows_WLAN-AUtoConfig/Operational
        ```
     2. Source
        ```markdown
        WLAN-AUtoConfig
        ```
     3. Event ID
        ```markdown
        8000
        ```
  2. At log on

  Actions:

  1. Program/Scripts
     ```markdown
     "path/to/pythonw.exe"
     ```
  2. Argumemt
     ```markdown
     "path/to/main.pyw"
     ```

---

# Debugging

In case if the script is broken, bebugging mode can be activated by passing in `-d` argument to the command

```markdown
$ python main.py -d
```

or

```markdown
$ python main.py --debug
```

---

# Limitation

Currently, only chrome browser is supported.

---

# FAQ

## How is the password stored?

Keyring library is used to store the password. The password will be stored in the [Windows Credentials Vault](https://stackoverflow.com/questions/14756352/how-is-python-keyring-implemented-on-windows).

---

# TODO

- [ ] Build task scheduler configuration
- [ ] Build GUI for setup configuration
