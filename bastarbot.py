from rozvrhy import get_rozvrh
from facebook_message import send_message, load
import time

email = "bastarbot@gmail.com"
password = "bastarbot2018"


period = 1

class User(object):
    def __init__(self, id, name, page, groups, classname, send_offset="40"):
        self.name = name
        self.page = page
        self.groups = groups + ["default"]
        self.classname = classname
        self.offset = send_offset

    def send(self, message):
        send_message(self.page, message)

    def send_lesson(self, index):
        rozvrh = get_rozvrh(self.classname)
        wday = time.localtime().tm_wday
        for lesson in rozvrh[wday]:
            if lesson.index == index and lesson.group in self.groups:
                hour = lesson
                send_message(self.page, "Předmět: %s \nUčitel: %s \nMístnost: %s \n"
                             % (hour.name, hour.teacher, hour.room))
                return True
        send_message(self.page, "Index Group mismatch")
        return False

    def day_hours(self, day_index):
        rozvrh = get_rozvrh(self.classname)
        wday = day_index
        day_hours = []
        for lesson in rozvrh[wday]:
            if lesson.group in self.groups:
                day_hours.append(lesson)
        return day_hours



users = \
    [
        User(1, "Otec", "https://www.messenger.com/t/ondrej.bastar.7", ["aj12", "fj2", "s2", "hv", "tvh"], "6.E"),
        User(2, "Kmotr", "https://www.messenger.com/t/hiep.michal", ["aj12", "nj21", "s1", "hv", "tvh"], "4.C"),
        User(3, "Zuzka", "https://www.messenger.com/t/zuzana.sobotkova.12", ["aj12", "fj2", "s1", "vv", "tvd"], "6.E"),
        User(4, "Dominik", "https://www.messenger.com/t/100018207906041", ["aj12", "fj2", "s2", "hv", "tvh"], "6.E"),
        User(5, "Gej", "https://www.messenger.com/t/tomas953", ["aj12", "nj22", "s2", "vv", "tvh"], "4.C"),
        User(6, "SexyBoi", "https://www.messenger.com/t/vitek.janca", ["aj12", "nj21", "s1", "hv", "tvh"], "4.C")
    ]

#test user
test_users = [User(1, "Otec", "https://www.messenger.com/t/ondrej.bastar.7", ["a12", "fj2", "s2", "hv", "tvh"], "6.E")]

# #enable testing by uncommenting
# users = test_users

lesson_starts = \
    {1: [7, 5],
     2: [8, 0],
     3: [8, 50],
     4: [9, 55],
     5: [10, 45],
     6: [11, 40],
     7: [12, 30],
     8: [13, 5],
     9: [13, 55],
     10: [14, 50],
     11: [15, 40]}


current_lesson = 1


def nice_strlist(l):
    l = str(l)
    l = l.strip("[")
    l = l.strip("]")
    l = l.replace("'", "")
    
    return l


def day_seconds(struct_time):
    hour = struct_time.tm_hour
    minute = struct_time.tm_min
    second = struct_time.tm_sec
    return hour * 3600 + minute * 60 + second


def time_to_seconds(hour, minute, second):
    return hour * 3600 + minute * 60 + second


def is_send_time(index):
    seconds_now = day_seconds(time.localtime())
    start_time = lesson_starts[index]
    start_time = time_to_seconds(start_time[0], start_time[1], 0)

    if abs(start_time + 45 * 60 - seconds_now) <= 60:
        return True


def mainloop():
    load(email, password)
    while True:
        #Sending timetables
        time_now = day_seconds(time.localtime())
        day = time.localtime().tm_wday
        time_now = 27900
        for i in lesson_starts.keys():
            if abs(time_to_seconds(lesson_starts[i][0], lesson_starts[i][1], 0) + 40*60 - time_now) <= period/1:
                for user in users:
                    user.send_lesson(i)
                    if i == 1:
                        user.send("Ahoj, %s, dnes tě čeká: \n %s \n Hodně zdaru! (PS: Pozdravuj ode mě Baštu)" %
                                  (user.name, nice_strlist([x.name for x in user.day_hours(day)])))
                break

        print(time.process_time())
        time.sleep(60)


mainloop()
