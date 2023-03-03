if 1 == 1:
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import time
from common.chrome import *
from dtos.gui_dto import GUIDto
from datetime import datetime
from common.utils import random_delay
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from common.utils import global_log_append
from selenium import webdriver
from timeit import default_timer as timer
from datetime import timedelta


class GoogleSearch:
    def __init__(self):
        # 현재 로컬에 저장된 크롬 기준으로 오픈한다.
        # open_browser()
        self.default_wait = 10
        self.driver = get_chrome_driver_new(is_headless=False, is_scret=True, move_to_corner=False)
        self.driver.implicitly_wait(self.default_wait)

    def setGuiDto(self, guiDto: GUIDto):
        self.guiDto = guiDto

    def setLogger(self, log_msg):
        self.log_msg = log_msg

    def search_google_img(self, google_keyword):
        driver = self.driver
        driver.get(f"https://www.google.co.kr/search?q={google_keyword}&hl=ko&tbm=isch")
        time.sleep(1)

    # 전체작업 시작
    def work_start(self):
        print(f"work_start")

        try:
            for google_keyword in self.guiDto.google_keyword_list:
                print(google_keyword)

                # 구글 이미지 검색
                # https://www.google.co.kr/search?q={키워드}&hl=ko&tbm=isch
                self.search_google_img(google_keyword)

        except Exception as e:
            print(str(e))
            self.log_msg.emit(str(e))
            print("구글 작업 실패")

        finally:
            time.sleep(1)


if __name__ == "__main__":

    searcher = GoogleSearch()
    searcher.work_start()
