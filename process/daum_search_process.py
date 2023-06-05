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
from selenium import webdriver
from common.utils import global_log_append
from timeit import default_timer as timer
from datetime import timedelta, datetime
from features.tistory_newspaper import TistoryNewsPaper
from dtos.top_blog_detail_dto import *
from config import *
import pandas as pd
import re
from docx import Document


class DaumSearch:
    def __init__(self):
        # 현재 로컬에 저장된 크롬 기준으로 오픈한다.
        # open_browser()
        self.default_wait = 10
        self.driver: webdriver.Chrome = get_chrome_driver_new(
            is_headless=True, is_secret=True, move_to_corner=False
        )
        self.driver.implicitly_wait(self.default_wait)
        self.run_time = str(datetime.now())[0:-10].replace(":", "")
        self.top_blog_detail_dtos = []


    def setGuiDto(self, guiDto: GUIDto):
        self.guiDto = guiDto

    def setLogger(self, log_msg):
        self.log_msg = log_msg


    def log_append(self, text:str):
        print('log_append', text)
        try:
            self.log_msg.emit(text)
        except:
            pass

    # 엑셀 저장
    def blog_detail_to_excel(self, top_blog_detail_dtos):
        article_excel = os.path.join(
            self.guiDto.search_file_save_path, f"상위노출데이터 {self.run_time}.xlsx"
        )
        pd.DataFrame.from_dict(top_blog_detail_dtos).to_excel(
            article_excel, index=False
        )
        time.sleep(1)

    # 워드 저장
    def blog_detail_to_docx(self, article_title: str, article_text: str, keyword: str):
        article_path = os.path.join(
            self.guiDto.search_file_save_path, f"글수집 {self.run_time}"
        )

        if os.path.isdir(article_path) == False:
            os.mkdir(article_path)
        else:
            pass

        keyword_img_path = os.path.join(article_path, f"{keyword}")
        if not os.path.isdir(keyword_img_path):
            os.mkdir(keyword_img_path)

        article_docx = os.path.join(keyword_img_path, f"{article_title}.docx")

        doc = Document()
        doc.add_paragraph(article_text)
        doc.save(article_docx)
        self.log_append(f"{article_title}.docx 저장 완료")

        time.sleep(1)

    def search_top_blog(self, daum_keyword: str):
        driver = self.driver
        driver.get(
            f"https://search.daum.net/search?w=fusion&col=blog&q={daum_keyword}&p=2"
        )

        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//c-card//c-title//a"))
            )
        except Exception as e:
            print(e)
            raise Exception(f"{daum_keyword}: 다음 검색 결과가 없습니다.")

        # 현재 페이지의 블로그 검색 결과
        # $x('//li[contains(@id, "br_tstory")]//a[contains(@class, "f_url")]')
        blog_links = driver.find_elements(By.XPATH, "//c-card//c-title//a")[:3]

        for blog_link in blog_links:
            blog_url = blog_link.get_attribute("href")
            print(blog_url)

            try:
                top_blog_detail_dto: TopBlogDetailDto = TistoryNewsPaper(
                ).get_article_detail(blog_url, daum_keyword)
            except Exception as e:
                print(e)
                top_blog_detail_dto = TopBlogDetailDto()
                top_blog_detail_dto.keyword = daum_keyword
                top_blog_detail_dto.article_title = driver.find_element(
                    By.XPATH,
                    f'//c-card//c-title//a[contains(@href, "{blog_url}")]',
                ).get_attribute("textContent")
                top_blog_detail_dto.article_text = "사이트 연결 오류"
                top_blog_detail_dto.article_url = blog_url

            try:
                # img_count = driver.find_element(
                #     By.XPATH, f'//a[contains(@href, "{blog_url}")]//c-badge-text/span'
                # ).get_attribute("textContent")
                if not top_blog_detail_dto.img_count:
                    top_thumnail_imgs = driver.find_elements(By.CSS_SELECTOR, f'a[class="thumb_bf"][href="{blog_url}"]')
                    img_count = len(top_thumnail_imgs)
                    top_blog_detail_dto.img_count = img_count
            except Exception as e:
                print(e)
                print("이미지 개수 탐색 실패")

            self.top_blog_detail_dtos.append(top_blog_detail_dto.get_dict())
            self.blog_detail_to_excel(self.top_blog_detail_dtos)

        time.sleep(1)

    def search_blog(self, daum_keyword: str):
        driver = self.driver
        search_blog_list = []

        for current_page in range(
            self.guiDto.daum_start_page, self.guiDto.daum_end_page + 1
        ):
            try:
                driver.get(
                    f"https://search.daum.net/search?w=fusion&col=blog&q={daum_keyword}&p={current_page}"
                )

                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//c-card//c-title//a"))
                )

                # 현재 페이지의 블로그 검색 결과
                # $x('//li[contains(@id, "br_tstory")]//a[contains(@class, "f_url")]')
                blog_list = driver.find_elements(By.XPATH, "//c-card")

                # 입력받은 날짜와 블로그 날짜를 비교합니다.
                search_date = self.guiDto.daum_search_date
                search_date_format = f"%Y-%m-%d"
                search_date = datetime.strptime(search_date, search_date_format)

                blog: webdriver.Chrome._web_element_cls
                for blog in blog_list:
                    blog_date = blog.find_element(
                        By.CSS_SELECTOR, 'span[class*="gem-subdesc"]'
                    ).get_attribute("textContent")
                    blog_date_format = f"%Y.%m.%d"

                    try:
                        blog_date = datetime.strptime(blog_date, blog_date_format)
                    except Exception as e:
                        print(f"날짜 형식에 맞지 않습니다.")
                        blog_date = datetime.now()

                    try:
                        is_naver_blog = blog.find_element(
                            By.CSS_SELECTOR, "c-title a"
                        ).get_attribute("href")
                        if is_naver_blog.find("naver.com") > -1:
                            raise Exception(f"네이버는 제외하고 진행합니다.")

                    except Exception as e:
                        print(str(e))
                        continue

                    if search_date > blog_date:
                        blog_url = blog.find_element(
                            By.CSS_SELECTOR, "c-title a"
                        ).get_attribute("href")

                        try:
                            top_blog_detail_dto: TopBlogDetailDto = TistoryNewsPaper(
                            ).get_article_detail(blog_url, daum_keyword)
                            top_blog_detail_dict = top_blog_detail_dto.get_dict()
                            article_text = top_blog_detail_dict["내용"]
                            article_title = (
                                f'{top_blog_detail_dict["제목"]} {str(blog_date)[:10]}'
                            )
                            article_title = re.sub('[\/:*?"<>|]', "", article_title)

                        except Exception as e:
                            print(e)
                            continue

                        # 워드 저장
                        self.blog_detail_to_docx(article_title, article_text, daum_keyword)

                        search_blog_list.append(article_title)

                        if len(search_blog_list) >= self.guiDto.daum_search_count:
                            self.log_append(f"{daum_keyword}: 수집할 글 개수에 도달했습니다.")
                            break

                    else:
                        # self.log_append(f"({search_date}) 보다 이후에 작성된 글입니다. ({blog_date})")
                        print(f"({search_date}) 보다 이후에 작성된 글입니다. ({blog_date})")
                        continue

                if len(search_blog_list) >= self.guiDto.daum_search_count:
                    print(f"{daum_keyword}: 수집할 글 개수에 도달했습니다.")
                    self.log_append(f"{daum_keyword}: 수집할 글 개수에 도달했습니다.")
                    break

            except Exception as e:
                self.log_append(f"{current_page}페이지 조회 실패")
                self.log_append(f"입력하신 페이지 수가 존재하지 않아 수집할 글 개수에 도달하지 못했습니다.")
                break

        if len(search_blog_list) == 0:
            self.log_append("입력하신 수집할 글 조건에 맞는 글이 없어 수집할 글 개수에 도달하지 못했습니다.")         
            
        time.sleep(1)

    # 전체작업 시작
    def work_start(self):
        print(f"daum_search_process: work_start")

        try:
            for daum_keyword in self.guiDto.daum_keyword_list:
                try:
                    self.log_append(f"{daum_keyword} 검색 시작")

                    # 구 블로그 검색 주소
                    # https://search.daum.net/search?w=blog&nil_search=btn&enc=utf8&q={검색어}&p=5

                    # 신 블로그 검색 주소
                    # https://search.daum.net/search?w=fusion&col=blog&q={검색어}&p=10

                    # 1. 다음 블로그 검색 후 최상단 3개의 글 수집
                    self.search_top_blog(daum_keyword)

                    # 2. 입력받은 페이지에서 입력한 갯수만큼 블로그 글 수집
                    self.search_blog(daum_keyword)
                    
                except Exception as e:
                    print(e)
                    self.log_append(str(e))
                    self.log_append(f"{daum_keyword} 수집 도중 오류가 발생하였습니다.")
                    continue

        except Exception as e:
            print(e)
            self.log_append(str(e))
            print(f"다음 작업 실패")

        finally:
            time.sleep(1)


if __name__ == "__main__":
    searcher = DaumSearch()
    searcher.work_start()
