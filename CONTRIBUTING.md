## Installation

Prerequisite:

- For `Windows` version:

    ```bash
    $ pip install -r win_requirements.txt
    ```
- For `Linux` version:
    
    ```bash
    $ pip install -r linux_requirements.txt
    ```
- Extra dependancies:

    ```bash
    $ pip install -r extra_requirements.txt
    ```

Clone this repo:

- Git

  ```markdown
  $ git clone https://github.com/jamestansx/autofi-utem.git
  ```

- GitHub CLI
  ```markdown
  $ gh repo clone jamestansx/autofi-utem
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
