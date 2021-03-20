import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def setupSelenium(driverPath, is_Connected):
    if is_Connected:
        chrome_option = Options()
        chrome_option.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_option.add_argument("--headless")
        chrome_option.add_argument("--ignore-certificate-errors")
        chrome_option.add_argument("--ignore-ssl-errors")
        chrome_option.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=driverPath, options=chrome_option)
        driver.implicitly_wait(3)
        return driver


def open_webdriver(driver, authUrl):
    try:
        driver.get(authUrl)
    except Exception:
        sys.exit(1)
