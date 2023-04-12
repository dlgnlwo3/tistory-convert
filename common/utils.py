import re
import random
import time
from datetime import datetime
import os
from config import LOG_FOLDER_PATH


# 전역 로그
def global_log_append(text):
    text = str(text)

    today = str(datetime.now())[0:10]
    now = str(datetime.now())[0:-7]

    log_path = LOG_FOLDER_PATH

    if os.path.isdir(log_path) == False:
        os.mkdir(log_path)
    else:
        pass

    today_log = os.path.join(log_path, f"{today}.txt")
    if os.path.isfile(today_log) == False:
        f = open(today_log, "w", encoding="UTF8")
    else:
        f = open(today_log, "a", encoding="UTF8")
    f.write(f"[{now}] {text}\n")
    f.close()


def random_delay(start, end):
    x = random.randint(start, end)
    time.sleep(x)


def check_common_element(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    intersection = set1 & set2
    return len(intersection) > 0
