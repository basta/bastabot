from rozvrhy import Rozvrh
from facebook_message import send_message, load
import time

email = "bastarbot@gmail.com"
password = "bastarbot2018"

first_lesson_seconds = 27300
period = 1


class User(object):
    def __init__(self, id, name, page, groups, classname, messages = [], send_offset="40"):
        self.id = id
        self.name = name
        self.page = page
        self.groups = groups + ["default"]
        self.classname = classname
        self.messages = messages
        self.offset = send_offset

    def send(self, message):
        send_message(self.page, message)

    def send_lesson(self, index, Rozvrhy):
        rozvrh = Rozvrhy[self.classname].get()
        wday = time.localtime().tm_wday
        for lesson in rozvrh[wday]:
            if lesson.index == index and lesson.group in self.groups:
                hour = lesson
                send_message(self.page, "Předmět: %s \nUčitel: %s \nMístnost: %s \n"
                             % (hour.name, hour.teacher, hour.room))
                return True
        send_message(self.page, "Index Group mismatch")
        return False

    def day_hours(self, day_index, Rozvrhy):
        rozvrh = Rozvrhy[self.classname].get()
        wday = day_index
        day_hours = []
        for lesson in rozvrh[wday]:
            if lesson.group in self.groups:
                day_hours.append(lesson)
        return day_hours


users = \
    [
        User(1, "Otec", "https://www.messenger.com/t/ondrej.bastar.7", ["a12", "fj2", "s2", "hv", "tvh"], "6.E"),
        User(2, "Kmotr", "https://www.messenger.com/t/hiep.michal", ["aj12", "nj21", "s1", "hv", "tvh"], "4.C"),
        User(3, "Zuzka", "https://www.messenger.com/t/zuzana.sobotkova.12", ["aj12", "fj2", "s1", "vv", "tvd"], "6.E"),
        User(4, "Dominik", "https://www.messenger.com/t/100018207906041", ["a12", "fj2", "s2", "hv", "tvh"], "6.E"),
        User(5, "Gej", "https://www.messenger.com/t/tomas953", ["aj12", "nj22", "s2", "vv", "tvh"], "4.C"),
        User(6, "SexyBoi", "https://www.messenger.com/t/vitek.janca", ["aj12", "fj2", "s1", "vv", "tvh"], "4.C")
    ]

#test user
test_users = [User(1, "Otec", "https://www.messenger.com/t/ondrej.bastar.7", ["a12", "fj2", "s2", "hv", "tvh"], "6.E")]

lesson_starts = \
    {1: [6, 55],
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



def create_Rozvrhy(users):
    Rozvrhy = {}
    for user in users:
        if user.classname not in Rozvrhy.keys():
            Rozvrhy[user.classname] = Rozvrh(user.classname)
    return Rozvrhy


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


def mainloop(email, password, users, Rozvrhy=[], custom_time=False, background=True, testing=False, output_to_log = False):
    load(email, password, background=background)

    if not Rozvrhy:
        Rozvrhy = create_Rozvrhy(users)
        for i in Rozvrhy.values():
            i.get()

    if output_to_log:
        log = open("log.txt", "a")

    if not testing:
        while True:

            #Sending timetables
            time_now = day_seconds(time.localtime())
            day = time.localtime().tm_wday

            if custom_time:
                time_now = custom_time
                if type(time_now) != int:
                    raise ValueError("Custom time must be integer")

            for i in lesson_starts.keys():
                if abs(time_to_seconds(lesson_starts[i][0], lesson_starts[i][1], 0) + 40*60 - time_now) <= 0.5:
                    for user in users:
                        user.send_lesson(i, Rozvrhy)
                        if i == 1:
                            user.send("Ahoj, %s, dnes tě čeká: \n %s \n Hodně zdaru!" %
                                      (user.name, nice_strlist([x.name for x in user.day_hours(day)])))

                                else:
                                    log.write("Ahoj, %s, dnes tě čeká: \n %s \n Hodně zdaru!" %
                                              (user.name, nice_strlist([x.name for x in user.day_hours(day)])))

                    break

                print(time_to_seconds(lesson_starts[i][0], lesson_starts[i][1], 0) + 40*60 - time_now)
            time.sleep(1)
    else:
        for custom_time in lesson_starts_seconds:
        # Sending timetables
            time_now = day_seconds(time.localtime())
            day = time.localtime().tm_wday

            if custom_time:
                time_now = custom_time
                if type(time_now) != int:
                    raise ValueError("Custom time must be integer")

            for i in lesson_starts.keys():
                if abs(time_to_seconds(lesson_starts[i][0], lesson_starts[i][1], 0) + 40 * 60 - time_now) <= 0.5:

                    for user in users:
                        user.send_lesson(i, Rozvrhy)

                        if i == 1:
                            if not output_to_log:
                                user.send("Ahoj, %s, dnes tě čeká: \n %s \n Hodně zdaru!" %
                                      (user.name, nice_strlist([x.name for x in user.day_hours(day)])))

                            else:
                                log.write("Ahoj, %s, dnes tě čeká: \n %s \n Hodně zdaru!" %
                                          (user.name, nice_strlist([x.name for x in user.day_hours(day)])))

                    break

                print(time_to_seconds(lesson_starts[i][0], lesson_starts[i][1], 0) + 40 * 60 - time_now)
            time.sleep(1)


lesson_starts_seconds = ["empty for indexing"]
for i in lesson_starts.values():
    lesson_starts_seconds.append(time_to_seconds(i[0], [1], 0))

if __name__ == "__main__":
    mainloop(email, password, users, custom_time=first_lesson_seconds, background=False)













