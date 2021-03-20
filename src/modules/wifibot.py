from selenium.common.exceptions import *

ignore_exceptions = (StaleElementReferenceException, NoSuchElementException)

def bot(driver, username, password):
    input_username(driver, username)
    input_password(driver, password)
    click_button(driver)
    isSuccess = is_success(driver)
    if isSuccess:
        driver.quit()
    else:
        print(isSuccess)
        driver.quit()



def input_username(driver, username):
    user_elem = driver.find_element_by_css_selector("#ID_formc5279f78_weblogin_user")
    user_elem.send_keys(username)

def input_password(driver, password):
    pass_elem = driver.find_element_by_css_selector("#ID_formc5279f78_weblogin_password")
    pass_elem.send_keys(password)

def click_button(driver):
    button = driver.find_element_by_css_selector("#ID_formc5279f78_weblogin_submit")
    button.click()

def is_success(driver):
    try:
        return driver.find_element_by_css_selector("body > font > b")
    except Exception as e:
        return e
