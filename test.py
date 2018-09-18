from bastarbot import mainloop, User
from facebook_message import send_message, load
from rozvrhy import get_rozvrh

users = [User("id", "Otec", "http://messenger.com/t/ondrej.bastar.7", ["4Bi", "aj11", "nj21"], "6.C")]
mainloop("bastarbot@gmail.com", "bastarbot2018", users, custom_time=32400)
