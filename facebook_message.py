from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from lxml import html
import time

email="bastarbot@gmail.com"
password = "bastarbot2018"

is_facebook_loaded = False


def load(email, password, background=True):
    global driver

    if background:
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(chrome_options=options)

    elif not background:
        driver = webdriver.Chrome()


    driver.get("http://www.messenger.com")

    email_element = driver.find_element_by_xpath("//input[@id='email']")
    password_element = driver.find_element_by_xpath("//input[@id='pass']")
    email_element.send_keys(email)
    password_element.send_keys(password)
    email_element.send_keys(Keys.RETURN)

    while driver.current_url == "http://messenger.com":
        time.sleep(0.1)

    print(driver.current_url)
    return driver


def day_seconds(struct_time):
    hour = struct_time.tm_hour
    minute = struct_time.tm_min
    second = struct_time.tm_sec
    return hour * 3600 + minute * 60 + second


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
