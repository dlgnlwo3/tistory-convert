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


class InstagramFollow:
    def __init__(self):
        # 현재 로컬에 저장된 크롬 기준으로 오픈한다.
        # open_browser()
        # self.driver = get_chrome_driver_new(is_headless=False, is_scret=True, move_to_corner=False)
        # self.driver.implicitly_wait(self.default_wait)
        self.default_wait = 10

        self.current_count = 0
        self.feed_url_list = []
        self.feedDtos = []
        self.accountDtos = []
        self.worked_feed_list = []
        self.worked_user_list = []

    def setGuiDto(self, guiDto: GUIDto):
        self.guiDto = guiDto

    def setLogger(self, log_msg):
        self.log_msg = log_msg

    # 로그인
    def login(self, id, pw, driver: webdriver.Chrome):
        print(f"{id} {pw} login")

        try:
            driver.get("https://www.instagram.com/accounts/login")
            time.sleep(2)

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//button[./div[contains(text(), "로그인")]]'))
            )
            time.sleep(1)

            input_id = driver.find_element(By.CSS_SELECTOR, 'input[name="username"]')
            input_id.clear()
            input_id.send_keys(id)
            time.sleep(1)

            input_pw = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
            input_pw.clear()
            input_pw.send_keys(pw)
            time.sleep(1)

            login_btn = driver.find_element(By.XPATH, '//button[./div[contains(text(), "로그인")]]')
            driver.execute_script("arguments[0].click();", login_btn)
            time.sleep(15)

            if driver.current_url.find("https://www.instagram.com/accounts/login") > -1:
                raise Exception(f"로그인에 실패했습니다.")

            # https://www.instagram.com/challenge/action -> 회원님이 계정의 소유자인지 확인해주세요
            if driver.current_url.find("https://www.instagram.com/challenge/action") > -1:
                raise Exception(f"계정 본인 인증 화면 발생")

            # 로그인 정보를 저장하시겠어요? 화면이 나왔다면 로그인 성공
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//button[contains(text(), "나중에 하기")]'))
            )
            driver.find_element(By.XPATH, '//button[contains(text(), "나중에 하기")]').click()
            time.sleep(1)

            # 홈 화면에 Instagram을 추가하시겠어요?
            try:
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, '//button[contains(text(), "홈 화면에 추가")]'))
                )
                driver.find_element(By.XPATH, '//button[contains(text(), "취소")]').click()
            except Exception as e:
                print(f"홈 화면에 Instagram을 추가하시겠어요?")
            time.sleep(1)

            # 알림 설정
            try:
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, '//button[contains(text(), "설정")]'))
                )
                driver.find_element(By.XPATH, '//button[contains(text(), "나중에 하기")]').click()
            except Exception as e:
                print(f"알림 설정")
            time.sleep(1)

        except Exception as e:
            print(e)
            print(f"{id}, {pw} 로그인에 실패했습니다.")
            raise Exception(f"{id}, {pw} 로그인에 실패했습니다. {str(e)}")

    # 탐색탭 -> 검색
    def search_keyword(self, driver: webdriver.Chrome):
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//a[contains(@href, "/explore")]')))
        driver.find_element(By.XPATH, '//a[contains(@href, "/explore")]').click()
        time.sleep(2)

        # 검색창 클릭
        search_button = driver.find_element(By.XPATH, '//span[contains(text(), "검색")]')
        driver.execute_script("arguments[0].click();", search_button)
        time.sleep(2)

        # 검색어 입력칸
        input_keyword = driver.find_element(By.XPATH, '//input[@placeholder="검색"]')
        input_keyword.send_keys(self.guiDto.keyword, Keys.ENTER)
        time.sleep(2)

        # 결과들 중 검색어와 일치하는 항목 클릭
        # $x('//a[.//div[./text()="#"][./text()="설득의심리학"]]')
        search_result = driver.find_element(By.XPATH, '//a[.//div[./text()="#"][./text()="설득의심리학"]]')
        driver.execute_script("arguments[0].click();", search_result)
        time.sleep(2)

    # 해시태그 검색 및 프로필 방문
    def search_keyword_for_work(self, driver: webdriver.Chrome, index):

        # driver.get(f"https://www.instagram.com/explore/tags/{self.guiDto.keyword}")
        # time.sleep(1)

        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//a[.//img][contains(@href, "p/")]')))
        time.sleep(1)

        # 최근 게시물만 들어있는 div
        # $x('//h2[contains(text(), "최근")]/following-sibling::div')
        recent_div = driver.find_element(By.XPATH, '//h2[contains(text(), "최근")]/following-sibling::div')
        time.sleep(1)

        recent_feeds = recent_div.find_elements(By.CSS_SELECTOR, "a")

        if index <= len(recent_feeds):
            try:
                driver.execute_script("arguments[0].click();", recent_feeds[index])
                time.sleep(2)

                WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, '//img[contains(@alt, "프로필 사진")]'))
                )
                time.sleep(1)

                try:
                    # 타겟 유저의 프로필인지 검증
                    target_profile = driver.find_element(
                        By.XPATH, f'//a[contains(text(), "{self.guiDto.target_name}")]'
                    )
                    time.sleep(1)

                    # 좋아요
                    try:
                        driver.implicitly_wait(2)
                        like_button = driver.find_element(By.XPATH, '//button[.//*[@aria-label="좋아요"]]')
                        driver.execute_script("arguments[0].click();", like_button)
                    except Exception as e:
                        print(f"이미 좋아요 상태입니다.")
                    finally:
                        driver.implicitly_wait(self.default_wait)
                        time.sleep(0.5)

                    # 저장
                    try:
                        driver.implicitly_wait(2)
                        save_button = driver.find_element(By.XPATH, '//button[.//*[@aria-label="저장"]]')
                        driver.execute_script("arguments[0].click();", save_button)
                    except Exception as e:
                        print(f"이미 저장 상태입니다.")
                    finally:
                        driver.implicitly_wait(self.default_wait)
                        time.sleep(0.5)

                    # 타겟 유저의 프로필 클릭
                    driver.execute_script("arguments[0].click();", target_profile)
                    time.sleep(3)

                    # 프로필 방문 후 일정시간 대기
                    random_delay(3, 5)

                    return True

                    # 타겟 유저 팔로우
                    try:
                        driver.implicitly_wait(5)
                        follow_button = driver.find_element(By.XPATH, '//header//button[.//*[contains(text(), "팔로우")]]')
                        driver.execute_script("arguments[0].click();", follow_button)
                    except Exception as e:
                        print(f"이미 팔로우 한 유저입니다.")
                    finally:
                        driver.implicitly_wait(self.default_wait)
                        time.sleep(0.5)

                except Exception as e:
                    return False

            except Exception as e:
                print(e)
                return False

        else:
            print(f"{self.guiDto.keyword} 최근 게시글 중 {self.guiDto.target_name} 유저가 없습니다.")
            self.log_msg.emit(f"{self.guiDto.keyword} 최근 게시글 중 {self.guiDto.target_name} 유저가 없습니다.")

    # 전체작업 시작
    def work_start(self):
        print(f"work_start")


if __name__ == "__main__":

    instagramCrawler = InstagramFollow()
    instagramCrawler.work_start()
