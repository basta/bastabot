from facebook_message import load
from lxml import html
from bastarbot import test_users
import time
from bastarbot import email, password


class Message(object):
    def __init__(self, id, content, time, user_id):
        self.id = id
        self.content = content
        self.time = time
        self.user_id = user_id


def listen(users):
    # if not "messenger.com/t/" in driver.current_url:
    #     raise NameError("Driver not on chat page")
    # messenger_source = html.fromstring(driver.page_source)
    # conversations_list = driver.find_element_by_xpath("//ul[@aria-label='Conversation List']")
    user_drivers = {}
    for usr in users:
        user_drivers[usr.id] = load(email, password, background=False).get(usr.page)
    for driver_id in user_drivers.keys():
        tree = html.fromstring(user_drivers[driver_id].page_source)
        # all_div = user_drivers[driver_id].find_elements_by_xpath("//div")
        print(user_drivers[driver_id].current_url)
        messages_elements = user_drivers[driver_id].find_elements_by_class_name("_29_7")
        print([x[0].get("body") for x in messages_elements])


if __name__ == "__main__":
    listen(test_users)

