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


class TistoryNewsPaper:
    def __init__(self, driver):
        self.driver: webdriver.Chrome = driver

    # 입력받은 url에서 이미지태그 개수와 키워드 반복횟수를 파악합니다.
    def get_article_from_blog_url(self, blog_url: str, keyword: str):
        driver = self.driver
        top_blog_detail_dto = TopBlogDetailDto()


        if blog_url.find(".com") > -1 and blog_url.find(".com/m/") == -1:
            blog_url = blog_url.replace(".com/", ".com/m/")
        elif blog_url.find(".org") > -1 and blog_url.find(".org/m/") == -1:
            blog_url = blog_url.replace(".org/", ".org/m/")
        elif blog_url.find(".kr") > -1 and blog_url.find(".kr/m/") == -1:
            blog_url = blog_url.replace(".kr/", ".kr/m/")

        print(f"{blog_url} {keyword}")

        driver.get(blog_url)

        article_title = ""

        try:
            driver.implicitly_wait(2)
            article_title = driver.find_element(
                By.CSS_SELECTOR, ".blogview_tit h3"
            ).get_attribute("textContent")
        except:
            pass

        # raise Exception("테스트")

        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0"

        config = Config()
        config.browser_user_agent = user_agent
        config.request_timeout = 15

        article = Article(blog_url, language="ko", config=config)
        article.download()
        article.parse()

        try:
            driver.implicitly_wait(2)
            content_img_els = driver.find_elements(By.CSS_SELECTOR, 'article img')


            content_img_list = []
            for content_img in content_img_els:
                img_src = content_img.get_attribute('src')
                if img_src.find('/thumb/') > - 1 or img_src.find('daumcdn.net/map') > - 1:
                    continue
                content_img_list.append(content_img)

            top_blog_detail_dto.img_count = str(len(content_img_list))
            
        except:
            pass


        article_url = article.url

        if not article_title:
            article_title = article.title

        if not article_title:
            article_title = keyword

        article_text = article.text
        article_html = article.html

        article_length = len(article_text.replace(" ", "").replace(f"\n", ""))

        keyword_count = article_text.count(keyword)
        # print(f"키워드 반복 횟수: {keyword_count}")

        # soup = BeautifulSoup(article_html, "html.parser")
        # img_tags = soup.find_all("img")
        # img_count = len(img_tags)
        # print(f"이미지 태그 개수: {img_count}")

        # clipboard.copy(str(article_text))

        top_blog_detail_dto.keyword = keyword
        top_blog_detail_dto.article_url = article_url
        top_blog_detail_dto.article_title = article_title
        top_blog_detail_dto.article_text = article_text
        top_blog_detail_dto.article_length = article_length
        top_blog_detail_dto.keyword_count = keyword_count
        # top_blog_detail_dto.img_count = img_count

        return top_blog_detail_dto


if __name__ == "__main__":

    blog_url = f"https://ruha007.tistory.com/95"
    keyword = "변비"
    driver = get_chrome_driver_new(is_headless=True, is_secret=True)

    newspaper = TistoryNewsPaper(driver)
    topBlogDetailDto = newspaper.get_article_from_blog_url(blog_url, keyword)
    topBlogDetailDto.to_print()
