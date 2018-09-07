from facebook_message import load
from lxml import html
import time
from bastarbot import test_users


class Message(object):
    def __init__(self, id, content, time, source_id):


driver = load("bastarbot@gmail.com", "bastarbot2018")
print(driver.get_cookies())

def listen(users):
    messenger_source = html.fromstring(driver.page_source)
    conversations_list = driver.find_elements_by_xpath("[//ul[@aria-label='Conversation List'")
    for chat in conversations_list:
        if chat.get("class") == "_5l-3 _1ht1 _1ht3":

