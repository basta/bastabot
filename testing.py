from bastarbot import mainloop, test_users, lesson_starts, User, create_Rozvrhy, email, password
from rozvrhy import Rozvrh

mainloop(email, password, test_users, background=False, testing= True, output_to_log= True)
