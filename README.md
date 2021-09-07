<h1 align="center">autofi-utem</h1>
<h4 align="center">An automation to authenticate login process to UTeM Kediaman_Pelajar WiFi</h4>
<div align="center">
  <img alt="GitHub" src="https://img.shields.io/github/license/jamestansx/autofi-utem?logo=lgtm&logoWidth=18&color=bright%20green">
  <img alt="LGTM Grade" src="https://img.shields.io/lgtm/grade/python/github/jamestansx/autofi-utem?logo=lgtm&logoWidth=18">
  <a href="https://lgtm.com/projects/g/jamestansx/autofi-utem/alerts/"><img alt="Total alerts" src="https://img.shields.io/lgtm/alerts/g/jamestansx/autofi-utem.svg?logo=lgtm&logoWidth=18"/></a>
</div>

---

# Installation

**UPDATE**


```
NO PREREQUISITE NEEDED
```

1. Download the executable from the [release page](https://github.com/jamestansx/autofi-utem/releases)
2. Run *setup.exe* to set up the configuration.

**Important**

Save the *main.exe* in a permanent path, so that the task scheduler will not break.

---
# Development

To build this project from source code, visit [this](contribution.md)

---

# FAQ

## How is the password stored?

Keyring library is used to store the password. The password will be stored in the [Windows Credentials Vault](https://stackoverflow.com/questions/14756352/how-is-python-keyring-implemented-on-windows).

---

# TODO

- [x] Build task scheduler configuration
