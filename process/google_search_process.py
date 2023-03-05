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
import urllib.request


class GoogleSearch:
    def __init__(self):
        # 현재 로컬에 저장된 크롬 기준으로 오픈한다.
        # open_browser()
        self.default_wait = 10
        self.driver = get_chrome_driver_new(is_headless=False, is_scret=True, move_to_corner=False)
        self.driver.implicitly_wait(self.default_wait)
        self.run_time = str(datetime.now())[0:-10].replace(":", "")

    def setGuiDto(self, guiDto: GUIDto):
        self.guiDto = guiDto

    def setLogger(self, log_msg):
        self.log_msg = log_msg

    # 이미지 저장
    def save_img_from_url(self, url: str, keyword: str, i: str):

        img_path = os.path.join(self.guiDto.search_file_save_path, f"이미지수집 {self.run_time}")
        if not os.path.isdir(img_path):
            os.mkdir(img_path)

        keyword_img_path = os.path.join(img_path, f"{keyword}")
        if not os.path.isdir(keyword_img_path):
            os.mkdir(keyword_img_path)

        img_format = url[url.find("data:image/") + 11 : url.find(";")]
        img_file = os.path.join(keyword_img_path, f"{keyword}{i.zfill(2)}.{img_format}")
        print(img_file)

        try:
            urllib.request.urlretrieve(url, img_file)

        except Exception as e:
            print(f"{url} 이미지 생성 실패 {e.msg}")
            global_log_append(f"{url} 이미지 생성 실패 {e.msg}")

        finally:
            time.sleep(0.2)

        return img_file

    def search_google_img(self, google_keyword):

        img_list = []

        driver = self.driver
        driver.get(f"https://www.google.co.kr/search?q={google_keyword}&hl=ko&tbm=isch")
        time.sleep(1)

        # 이미지가 있으면...
        # $x('//div/h3/following-sibling::a[1]//img')
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div/h3/following-sibling::a[1]//img"))
        )

        img_urls = driver.find_elements(By.XPATH, "//div/h3/following-sibling::a[1]//img")

        for i, img_url in enumerate(img_urls):
            img_url = img_url.get_attribute("src")

            img_file = self.save_img_from_url(img_url, google_keyword, str(i + 1))

            img_list.append(img_file)

            if len(img_list) >= self.guiDto.google_search_count:
                print("수집할 이미지 개수에 도달했습니다.")
                break

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
