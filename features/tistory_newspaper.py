if 1 == 1:
    import sys
    import warnings
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    warnings.simplefilter("ignore", UserWarning)
    sys.coinit_flags = 2

from newspaper import Article
from newspaper import Config
import os
import clipboard
from bs4 import BeautifulSoup
from dtos.top_blog_detail_dto import *
from selenium import webdriver
from common.chrome import get_chrome_driver_new
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import requests

class TistoryNewsPaper:
    def __init__(self):
        self.driver = get_chrome_driver_new(is_headless=True, is_secret=True)

    def get_title_and_img_count(self, blog_url:str):
        
        article_title = ""
        img_count = 0 

        driver = self.driver
        driver.get(blog_url)

        if blog_url.find(".com") > -1 and blog_url.find(".com/m/") == -1:
            blog_url = blog_url.replace(".com/", ".com/m/")
        elif blog_url.find(".org") > -1 and blog_url.find(".org/m/") == -1:
            blog_url = blog_url.replace(".org/", ".org/m/")
        elif blog_url.find(".kr") > -1 and blog_url.find(".kr/m/") == -1:
            blog_url = blog_url.replace(".kr/", ".kr/m/")

        try:
            driver.implicitly_wait(2)
            article_title = driver.find_element(
                By.CSS_SELECTOR, ".blogview_tit h3"
            ).get_attribute("textContent")
        except:
            pass

        try:
            driver.implicitly_wait(2)
            content_img_els = driver.find_elements(By.CSS_SELECTOR, 'article img')
            content_img_list = []
            for content_img in content_img_els:
                img_src = content_img.get_attribute('src')
                if img_src.find('/thumb/') > - 1 or img_src.find('daumcdn.net/map') > - 1:
                    continue
                content_img_list.append(content_img)

            img_count = str(len(content_img_list))
            
        except:
            pass
        
        self.driver.quit()

        return article_title, img_count


    # 입력받은 url에서 이미지태그 개수와 키워드 반복횟수를 파악합니다.
    def get_article_text_and_url(self, blog_url: str):

        response = requests.get(blog_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        div_soup = soup.find("div", class_="tt_article_useless_p_margin")
        article_url = response.url
        article_text = div_soup.text

        return article_text, article_url

    # 입력받은 url에서 이미지태그 개수와 키워드 반복횟수를 파악합니다.
    def get_article_detail(self, blog_url: str, keyword: str):
        top_blog_detail_dto = TopBlogDetailDto()

        article_title, img_count = self.get_title_and_img_count(blog_url)
        if not article_title:
            article_title = keyword

        article_text, article_url = self.get_article_text_and_url(blog_url)

        article_text = str(article_text)
        article_length = len(article_text.replace(" ", "").replace(f"\n", ""))
        keyword_count = str(article_text).count(keyword)


        top_blog_detail_dto.keyword = keyword
        top_blog_detail_dto.article_url = article_url
        top_blog_detail_dto.article_title = article_title
        top_blog_detail_dto.article_text = article_text
        top_blog_detail_dto.article_length = article_length
        top_blog_detail_dto.keyword_count = keyword_count
        top_blog_detail_dto.img_count = img_count

        return top_blog_detail_dto


if __name__ == "__main__":

    blog_url = f"https://ruha007.tistory.com/95"
    keyword = "변비"
    driver = get_chrome_driver_new(is_headless=True, is_secret=True)

    newspaper = TistoryNewsPaper()
    topBlogDetailDto = newspaper.get_article_detail(blog_url, keyword)
    topBlogDetailDto.to_print()
