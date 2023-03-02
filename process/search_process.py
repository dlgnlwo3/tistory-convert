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


class Search:
    def __init__(self):
        # 현재 로컬에 저장된 크롬 기준으로 오픈한다.
        # open_browser()
        # self.driver = get_chrome_driver_new(is_headless=False, is_scret=True, move_to_corner=False)
        # self.driver.implicitly_wait(self.default_wait)
        self.default_wait = 10

    def setGuiDto(self, guiDto: GUIDto):
        self.guiDto = guiDto

    def setLogger(self, log_msg):
        self.log_msg = log_msg

    # 전체작업 시작
    def work_start(self):
        print(f"work_start")


if __name__ == "__main__":

    searcher = Search()
    searcher.work_start()
