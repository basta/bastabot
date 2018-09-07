from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from lxml import html
import time

email="bastarbot@gmail.com"
password = "bastarbot2018"

is_facebook_loaded = False

def load(email, password):
    global driver
    driver = webdriver.Chrome()
    try:
        driver.get("http://www.messenger.com")
        email_element = driver.find_element_by_xpath("//input[@id='email']")
        password_element = driver.find_element_by_xpath("//input[@id='pass']")
        email_element.send_keys(email)
        password_element.send_keys(password)
        email_element.send_keys(Keys.RETURN)
        while driver.current_url == "http://messenger.com":
            time.sleep(0.1)
        print(driver.get_cookies())
        return driver
    except selenium.common.exceptions.ElementNotVisibleException:
        load(email, password)
        print("something not found")




def send_message(user_page, message):
    driver.get(user_page)
    message_field = driver.find_element_by_xpath("//div[@aria-label='Type a message...']")
    message_field.send_keys(message)
    message_field.send_keys(Keys.RETURN)
    time.sleep(1)


if __name__ == "__main__":
    print("ahoj")
    load(email, password)
    input()
    send_message("https://www.messenger.com/t/ondrej.bastar.7", "Ahoj \n ahoj")
