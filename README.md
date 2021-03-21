# autofi-utem

Automatically authenticate login process to UTeM Kediaman_Pelajar WiFi

---

# Installation

Prerequisite:

- python version > 3.6.x
- libraries in requirements.txt
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

# Usage

### Setup configuration

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

### Scheduler Setup

- **Windows**

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

# Limitation

Currently, only chrome browser is supported.

---

# FAQ

## How is the password stored?

Keyring library is used to store the password. The password will be stored in the [Windows Credentials Vault](https://stackoverflow.com/questions/14756352/how-is-python-keyring-implemented-on-windows).
