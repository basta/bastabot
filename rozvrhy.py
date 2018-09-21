from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium.exceptions import NoSuchElementException
from lxml import html
import time


def clean_end(self):
    for day in range(len(self.value)):
        index = -1
        while self.value[day][index].name != "Volná hodina":
            index += -1
        self.value[day] = self.value[day][:-index]


def day_seconds(struct_time):
    hour = struct_time.tm_hour
    minute = struct_time.tm_min
    second = struct_time.tm_sec
    return hour * 3600 + minute * 60 + second


class Rozvrh(object):
    def __str__(self):
        rozvrh = self.get()
        out = ""
        for i in rozvrh:
            out += str([x.name for x in i])
            out += "\n"
        return out

    def __init__(self, classname):
        self.classname = classname
        self.is_first = True
        self.refresh_time = 0

    def _refresh(self):
        driver = webdriver.Chrome()
        driver.get("https://bakalari.mikulasske.cz/rozvrh.aspx")

        # Opens correct timetable
        class_pick = driver.find_element_by_id("combotrida_I")
        class_pick.clear()
        class_pick = driver.find_element_by_id("combotrida_I")
        class_pick.send_keys(self.classname)
        class_pick.send_keys(Keys.RETURN)

        # gets lesson data
        while True:
            try:
                timetable_tree = html.fromstring(driver.page_source)
                break
            except:
                print("Error: Page source not found. Trying again...")
                time.sleep(0.1)

        days_elements = timetable_tree.xpath("//table[@class='r_roztable']/tbody/tr")
        days = []

        for day_element in days_elements:
            day = []
            index = 0
            for lesson in day_element:
                try:
                    temp = lesson[0]
                    # Classic lesson
                    if lesson[0].get("class") == "r_bunka":
                        group = "default"
                        name = (lesson[0][0].get("title"))
                        teacher = lesson[0][1].get("title")
                        if lesson[0][2].get("class") == "r_mist":
                            room = lesson[0][2][0].text
                        elif lesson[0][3].get("class") == "r_mist":
                            room = lesson[0][3][0].text
                            group = lesson[0][2][0].text
                        day.append(Hour(name, teacher, room, index, group=group))

                    # Free lesson
                    elif lesson.get("class") == "r_rr":
                        name = ("Volná hodina")
                        teacher = ("Volná hodina")
                        room = ("Volná hodina")
                        day.append(Hour(name, teacher, room, index))

                    # Divided lessons
                    elif "r_bunka_" in temp.get("class"):
                        for cell in lesson[0]:
                            name = (cell[0].get("title"))
                            teacher = (cell[0][1].get("title"))
                            group = cell[2][0].text
                            room = cell[3][0].text
                            day.append(Hour(name, teacher, room, index, group=group))


                    #
                    # #Divided lesson
                    # elif lesson[0].get("class") == "r_bunka_2":
                    #     #Upper part
                    #     name = (lesson[0][0][0].get("title"))
                    #     teacher = (lesson[0][0][1].get("title"))
                    #     group = lesson[0][0][2][0].text
                    #     room = lesson[0][0][3][0].text
                    #     day.append(Hour(name, teacher, room, index, group=group))
                    #
                    #     #Lower part
                    #     name = (lesson[0][1][0].get("title"))
                    #     teacher = (lesson[0][1][1].get("title"))
                    #     group = lesson[0][1][2][0].text
                    #     room = lesson[0][1][3][0].text
                    #     day.append(Hour(name, teacher, room, index, group=group))
                    #
                    # #Triple divided lesson
                    # elif lesson[0].get("class") == "r_bunka_3":
                    #     #1 part
                    #     name = (lesson[0][0][0].get("title"))
                    #     teacher = (lesson[0][0][1].get("title"))
                    #     group = lesson[0][0][2][0].text
                    #     room = lesson[0][0][3][0].text
                    #     day.append(Hour(name, teacher, room, index, group=group))
                    #
                    #     #2 part
                    #     name = (lesson[0][1][0].get("title"))
                    #     teacher = (lesson[0][1][1].get("title"))
                    #     group = lesson[0][1][2][0].text
                    #     room = lesson[0][1][3][0].text
                    #     day.append(Hour(name, teacher, room, index, group=group))
                    #
                    #     #3 part
                    #     name = (lesson[0][2][0].get("title"))
                    #     teacher = (lesson[0][2][1].get("title"))
                    #     group = lesson[0][2][2][0].text
                    #     room = lesson[0][2][3][0].text
                    #     day.append(Hour(name, teacher, room, index, group=group))

                    # Changed lesson
                    elif lesson[0].get("class") == "r_bunkazm":
                        group = "default"
                        name = (lesson[0][1].get("title"))
                        teacher = lesson[0][2].get("title")
                        if lesson[0][3].get("class") == "r_mist":
                            room = lesson[0][3][0].text
                        elif lesson[0][4].get("class") == "r_mist":
                            room = lesson[0][4][0].text
                            group = lesson[0][2][0].text
                        day.append(Hour(name, teacher, room, index, group=group, changed=True))
                    # Canceled/Special lesson
                    elif lesson[0].get("class") == "r_bunkamo":
                        name = lesson[0][0].get("title")
                        teacher = "N/A"
                        room = "N/A"
                        day.append(Hour(name, teacher, room, index))

                    else:
                        day.append(Hour("-----", "-----", "-----", index))
                    index += 1

                except IndexError:
                    print("something not found")

            days.append(day)

        # Formatting
        # for i in range(len(days)):
        #     days[i] = days[i][1:]
        days = days[1:]
        driver.close()
        self.value = days
        self.clean_end()
        self.refresh_time = day_seconds(time.localtime())
        self.is_first = False

    def get(self):
        freshness = day_seconds(time.localtime()) - self.refresh_time
        if self.is_first or freshness > 2400 or freshness < 0:
            self._refresh()
        return self.value

    def clean_end(self):
        for day in range(len(self.value)):
            index = -1
            while self.value[day][index].name != "Volná hodina":
                index += -1
            self.value[day] = self.value[day][:-index]


class Hour(object):
    def __init__(self, name, teacher, room, index, group = "default", changed=False):
        self.name = name
        self.teacher = teacher
        self.room = room
        self.group = group
        self.index = index


def get_rozvrh(trida):
    driver = webdriver.Chrome()
    driver.get("https://bakalari.mikulasske.cz/rozvrh.aspx")

    #Opens correct timetable
    class_pick = driver.find_element_by_id("combotrida_I")
    class_pick.clear()
    class_pick = driver.find_element_by_id("combotrida_I")
    class_pick.send_keys(trida)
    class_pick.send_keys(Keys.RETURN)

    #gets lesson data
    while True:
        try:
            timetable_tree = html.fromstring(driver.page_source)
            break
        except:
            print("Error: Page source not found. Trying again...")
            time.sleep(0.1)

    days_elements = timetable_tree.xpath("//table[@class='r_roztable']/tbody/tr")
    days = []

    for day_element in days_elements:
        day = []
        index = 0
        for lesson in day_element:
            try:
                temp = lesson[0]
                #Classic lesson
                if lesson[0].get("class") == "r_bunka":
                    group = "default"
                    name = (lesson[0][0].get("title"))
                    teacher = lesson[0][1].get("title")
                    if lesson[0][2].get("class") == "r_mist":
                        room = lesson[0][2][0].text
                    elif lesson[0][3].get("class") == "r_mist":
                        room = lesson[0][3][0].text
                        group = lesson[0][2][0].text
                    day.append(Hour(name, teacher, room, index, group=group))

                #Free lesson
                elif lesson.get("class") == "r_rr":
                    name = ("Volná hodina")
                    teacher = ("Volná hodina")
                    room = ("Volná hodina")
                    day.append(Hour(name, teacher, room, index))

                #Divided lessons
                elif "r_bunka_" in temp.get():
                    for cell in lesson[0]:
                        name = (cell[0].get("title"))
                        teacher = (cell[0][1].get("title"))
                        group = cell[2][0].text
                        room = cell[3][0].text
                        day.append(Hour(name, teacher, room, index, group=group))


                #
                # #Divided lesson
                # elif lesson[0].get("class") == "r_bunka_2":
                #     #Upper part
                #     name = (lesson[0][0][0].get("title"))
                #     teacher = (lesson[0][0][1].get("title"))
                #     group = lesson[0][0][2][0].text
                #     room = lesson[0][0][3][0].text
                #     day.append(Hour(name, teacher, room, index, group=group))
                #
                #     #Lower part
                #     name = (lesson[0][1][0].get("title"))
                #     teacher = (lesson[0][1][1].get("title"))
                #     group = lesson[0][1][2][0].text
                #     room = lesson[0][1][3][0].text
                #     day.append(Hour(name, teacher, room, index, group=group))
                #
                # #Triple divided lesson
                # elif lesson[0].get("class") == "r_bunka_3":
                #     #1 part
                #     name = (lesson[0][0][0].get("title"))
                #     teacher = (lesson[0][0][1].get("title"))
                #     group = lesson[0][0][2][0].text
                #     room = lesson[0][0][3][0].text
                #     day.append(Hour(name, teacher, room, index, group=group))
                #
                #     #2 part
                #     name = (lesson[0][1][0].get("title"))
                #     teacher = (lesson[0][1][1].get("title"))
                #     group = lesson[0][1][2][0].text
                #     room = lesson[0][1][3][0].text
                #     day.append(Hour(name, teacher, room, index, group=group))
                #
                #     #3 part
                #     name = (lesson[0][2][0].get("title"))
                #     teacher = (lesson[0][2][1].get("title"))
                #     group = lesson[0][2][2][0].text
                #     room = lesson[0][2][3][0].text
                #     day.append(Hour(name, teacher, room, index, group=group))

                #Changed lesson
                elif lesson[0].get("class") == "r_bunkazm":
                    group = "default"
                    name = (lesson[0][1].get("title"))
                    teacher = lesson[0][2].get("title")
                    if lesson[0][3].get("class") == "r_mist":
                        room = lesson[0][3][0].text
                    elif lesson[0][4].get("class") == "r_mist":
                        room = lesson[0][4][0].text
                        group = lesson[0][2][0].text
                    day.append(Hour(name, teacher, room, index, group=group, changed=True))
                #Canceled/Special lesson
                elif lesson[0].get("class") == "r_bunkamo":
                    name = lesson[0][0].get("title")
                    teacher = "N/A"
                    room = "N/A"
                    day.append(Hour(name, teacher, room, index))

                else:
                    day.append(Hour("-----", "-----", "-----", index))
                index += 1

            except IndexError:
                print("something not found")

        days.append(day)

    #Formatting
    # for i in range(len(days)):
    #     days[i] = days[i][1:]
    days = days[1:]
    driver.close()
    return days


if __name__ == "__main__":
    print(Rozvrh("6.E"))