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
import hashlib
import uuid


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


def get_word_count_without_empty(text: str) -> int:
    nospace = re.sub("&nbsp;| |\t|\r|\n", "", text)
    return len(nospace)


def get_word_count_without_empty2(article_text: str) -> int:
    return len(article_text.replace("\xa0", "").replace(" ", "").replace(f"\n", "").replace(f"\t", ""))


def get_word_count_from_html(html: str, convert_hint: str):
    soup = BeautifulSoup(html, "html.parser")
    before_total_count = get_word_count_without_empty(soup.get_text())
    converted_word_count = 0
    # Find all <span> elements with style="color: red"
    red_spans = soup.find_all("span", style=lambda value: value and convert_hint in value)
    for span in red_spans:
        converted_word_count += get_word_count_without_empty(str(span.text))

    return before_total_count, converted_word_count


def get_mac_address():
    return getmac.get_mac_address()


import math


def is_empty_or_nan(value):
    if isinstance(value, float) and math.isnan(value):
        return True

    if isinstance(value, str) and not value.strip():
        return True

    if isinstance(value, (list, dict, tuple, set)) and not value:
        return True

    return False


def remove_empty_item(items: list):
    for item in items:
        if is_empty_or_nan(item):
            items.remove(item)
    return items


import re


def convert_multiple_newlines(string):
    # converted_string = re.sub('\n{3,}', '\n\n', string)
    converted_string = re.sub(r"(\n\s*){3,}", "\n\n", string)
    return converted_string


def filter_article_content(article_text: str):
    # Remove advertisements
    ad_patterns = [
        r"<!--\s*google_ad_section_start.*?google_ad_section_end\s*-->",  # Match Google ad sections
        r"<script[^>]*>.*?googlesyndication\.com.*?</script>",  # Match Google ad scripts
        r"<iframe[^>]*src=\".*?googleadservices\.com.*?</iframe>",  # Match Google ad iframes
        # Add more patterns for Google ads as needed
    ]

    for pattern in ad_patterns:
        article_text = re.sub(pattern, "", article_text)

    # Remove links
    article_text = re.sub(r"<a\b[^>]*>(.*?)</a>", "", article_text)

    # Remove image alt information
    article_text = re.sub(r"<img[^>]*alt=\"(.*?)\"[^>]*>", "", article_text)

    # over empty 3lines to 2lines
    article_text = convert_multiple_newlines(article_text)

    # Remove extra whitespace
    # article_text = re.sub(r"\s+", " ", article_text.strip())

    return article_text


def escape_xml_string(s):
    s = re.sub("[\\x00-\\x08\\x0b\\x0e-\\x1f\\x7f]", "", s)
    return s


def get_new_token():
    timestamp = str(int(time.time()))
    software_id = str(uuid.uuid4())
    license_data = timestamp + software_id
    return hashlib.sha256(license_data.encode()).hexdigest()


def destroy_parent_widgets(widget):
    parent = widget.parentWidget()
    while parent is not None:
        parent.deleteLater()
        parent = parent.parentWidget()


def get_unique_name(names: list, name: str) -> str:
    unique_name = name
    original_name = name
    counter = 1
    while name in names:
        unique_name = f"{original_name} ({counter})"
        counter += 1
    return unique_name


def find_next_available_name(names, name):
    new_name = name
    counter = 1
    while new_name in names:
        new_name = f"{name} ({counter})"
        counter += 1
    return new_name


if __name__ == "__main__":
    names = ["a", "a (1)", "b", "c"]
    name_to_add = "a"

    next_available_name = find_next_available_name(names, name_to_add)
    print(next_available_name)
