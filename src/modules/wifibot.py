from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from modules.settings import log
from modules import wifiauth

ignore_exceptions = (StaleElementReferenceException, NoSuchElementException)


def bot(driver, username, password, isDebug=False):
    try:
        logger = log.newLogging("log.log", isDebug=isDebug)
        input_username(driver, username, logger)
        input_password(driver, password, logger)
        click_button(driver, logger)
        isSuccess = wifiauth.is_Connected()
        if isSuccess:
            if isDebug:
                input("Press enter to continue")
            driver.quit()
        else:
            logger.critical(f"Failed to authenticate--\n{isSuccess}\n")
            if isDebug:
                input("Press enter to continue")
            driver.quit()
    except:
        logger.exception(f"Exception: ")
        driver.quit()


def input_username(driver, username, logger):
    user_elem = driver.find_element_by_css_selector("#ID_formc5279f78_weblogin_user")
    user_elem.send_keys(username)
    logger.info("username is entered\n")


def input_password(driver, password, logger):
    pass_elem = driver.find_element_by_css_selector("#ID_formc5279f78_weblogin_password")
    pass_elem.send_keys(password)
    logger.info("password is entered\n")


def click_button(driver, logger):
    button = driver.find_element_by_css_selector("#ID_formc5279f78_weblogin_submit")
    button.click()
    logger.info("submit button is clicked\n")
