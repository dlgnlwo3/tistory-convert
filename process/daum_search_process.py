if 1 == 1:
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import time
from dtos.gui_dto import GUIDto
from common.utils import random_delay
from common.chrome import get_chrome_driver_new
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from common.utils import global_log_append
from timeit import default_timer as timer
from datetime import timedelta, datetime
from features.tistory_newspaper import TistoryNewsPaper
from dtos.top_blog_detail_dto import *
from config import *
import pandas as pd


class DaumSearch:
    def __init__(self):
        # 현재 로컬에 저장된 크롬 기준으로 오픈한다.
        # open_browser()
        self.default_wait = 10
        self.driver = get_chrome_driver_new(is_headless=False, is_scret=True, move_to_corner=False)
        self.driver.implicitly_wait(self.default_wait)
        self.run_time = str(datetime.now())[0:-10].replace(":", "")
        self.top_blog_detail_dtos = []

    def setGuiDto(self, guiDto: GUIDto):
        self.guiDto = guiDto

    def setLogger(self, log_msg):
        self.log_msg = log_msg

    # 엑셀 저장
    def blog_detail_to_excel(self, top_blog_detail_dtos):
        article_excel = os.path.join(self.guiDto.search_file_save_path, f"상위노출데이터 {self.run_time}.xlsx")
        pd.DataFrame.from_dict(top_blog_detail_dtos).to_excel(article_excel, index=False)
        time.sleep(1)

    def search_top_blog(self, daum_keyword: str):
        driver = self.driver
        driver.get(f"https://search.daum.net/search?w=blog&nil_search=btn&enc=utf8&q={daum_keyword}&p=1")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//li[contains(@id, "br_tstory")]//a[contains(@class, "f_url")]'))
        )

        # 현재 페이지의 블로그 검색 결과
        # $x('//li[contains(@id, "br_tstory")]//a[contains(@class, "f_url")]')
        blog_links = driver.find_elements(By.XPATH, '//li[contains(@id, "br_tstory")]//a[contains(@class, "f_url")]')[
            :3
        ]

        for blog_link in blog_links:
            blog_url = blog_link.get_attribute("href")

            # newspaper3k로 진행
            top_blog_detail_dto: TopBlogDetailDto = TistoryNewsPaper().get_article_from_blog_url(blog_url, daum_keyword)
            self.top_blog_detail_dtos.append(top_blog_detail_dto.get_dict())
            self.blog_detail_to_excel(self.top_blog_detail_dtos)

        time.sleep(1)

    def search_blog(self, daum_keyword: str):
        driver = self.driver

        search_blog_list = []

        for current_page in range(self.guiDto.daum_start_page, self.guiDto.daum_end_page + 1):
            driver.get(
                f"https://search.daum.net/search?w=blog&nil_search=btn&enc=utf8&q={daum_keyword}&p={current_page}"
            )

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//li[contains(@id, "br_tstory")]//a[contains(@class, "f_url")]'))
            )

            # 현재 페이지의 블로그 검색 결과
            # $x('//li[contains(@id, "br_tstory")]//a[contains(@class, "f_url")]')
            blog_links = driver.find_elements(
                By.XPATH, '//li[contains(@id, "br_tstory")]//a[contains(@class, "f_url")]'
            )

            print(self.guiDto.daum_search_date)
            print()

            if len(search_blog_list) >= self.guiDto.daum_search_count:
                print(f"수집할 글 개수에 도달했습니다.")
                break

        time.sleep(1)

    # 전체작업 시작
    def work_start(self):
        print(f"daum_search_process: work_start")

        try:
            for daum_keyword in self.guiDto.daum_keyword_list:
                print(daum_keyword)

                # 검색어 블로그 주소
                # https://search.daum.net/search?w=blog&nil_search=btn&enc=utf8&q={검색어}&p=5
                # 1. 다음 블로그 검색 후 최상단 3개의 글 수집
                self.search_top_blog(daum_keyword)

                # 2. 입력받은 페이지에서 입력한 갯수만큼 블로그 글 수집
                self.search_blog(daum_keyword)

        except Exception as e:
            print(e)
            self.log_msg.emit(str(e))
            print(f"다음 작업 실패")

        finally:
            time.sleep(1)


if __name__ == "__main__":

    searcher = DaumSearch()
    searcher.work_start()
