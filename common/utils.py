if 1 == 1:
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


import re
import random
import time
from datetime import datetime
import os
from config import LOG_FOLDER_PATH
import winsound as ws
from bs4 import BeautifulSoup
import getmac


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


def os_system_shutdown():
    os.system("shutdown /s /t 5")


def beepsound():
    freq = 500  # range : 37 ~ 32767
    dur = 1500  # ms
    ws.Beep(freq, dur)  # winsound.Beep(frequency, duration)



def get_word_count_without_empty(text:str) -> int:
    nospace = re.sub('&nbsp;| |\t|\r|\n', '', text)
    return len(nospace)


def get_word_count_from_html(html:str, convert_hint:str):
    
    soup = BeautifulSoup(html, "html.parser")
    before_total_count = get_word_count_without_empty(soup.get_text())
    converted_word_count = 0
    # Find all <span> elements with style="color: red"
    red_spans = soup.find_all('span', style=lambda value: value and convert_hint in value)
    for span in red_spans:
        converted_word_count += get_word_count_without_empty(str(span.text))

    return before_total_count, converted_word_count



def get_mac_address():
    return getmac.get_mac_address()


if __name__ == "__main__":
    print(get_mac_address())
