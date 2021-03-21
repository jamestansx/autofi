from selenium.common.exceptions import *
from src.modules.settings import log

ignore_exceptions = (StaleElementReferenceException, NoSuchElementException)

def bot(driver, username, password):
    logger = log.newLogging("log.log")
    input_username(driver, username)
    input_password(driver, password)
    click_button(driver)
    isSuccess = is_success(driver)
    if isSuccess:
        driver.quit()
    else:
        logger.critical(f"Failed to authenticate--\n{isSuccess}")
        driver.quit()



def input_username(driver, username, logger):
    user_elem = driver.find_element_by_css_selector("#ID_formc5279f78_weblogin_user")
    user_elem.send_keys(username)
    logger.info("username is entered")

def input_password(driver, password, logger):
    pass_elem = driver.find_element_by_css_selector("#ID_formc5279f78_weblogin_password")
    pass_elem.send_keys(password)
    logger.info("password is entered")

def click_button(driver, logger):
    button = driver.find_element_by_css_selector("#ID_formc5279f78_weblogin_submit")
    button.click()
    logger.info("submit button is clicked")

def is_success(driver, logger):
    try:
        driver.find_element_by_css_selector("body > font > b")
        logger.info("WiFi is successfully authenticated")
        return True
    except Exception as e:
        return e
