if 1 == 1:
    import sys
    import warnings
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    warnings.simplefilter("ignore", UserWarning)
    sys.coinit_flags = 2

import os
import clipboard
from dtos.top_blog_detail_dto import *
from selenium import webdriver
from newspaper import Article
from newspaper import Config
from bs4 import BeautifulSoup
import requests


class TistoryBeautifulsoup:
    def __init__(self):
        pass

    # 입력받은 url에서 이미지태그 개수와 키워드 반복횟수를 파악합니다.
    def get_article_from_blog_url(self, blog_url: str, keyword: str):
        top_blog_detail_dto = TopBlogDetailDto()

        print(f"{blog_url} {keyword}")

        # raise Exception("테스트")

        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0"

        config = Config()
        config.browser_user_agent = user_agent
        config.request_timeout = 15

        article = Article(blog_url, language="ko", config=config)
        article.download()
        article.parse()

        article_url = article.url
        article_title = article.title
        article_text = article.text
        article_html = article.html

        article_length = len(article_text)

        keyword_count = article_text.count(keyword)
        # print(f"키워드 반복 횟수: {keyword_count}")

        # soup = BeautifulSoup(article_html, "html.parser")
        # img_tags = soup.find_all("img")
        # img_count = len(img_tags)
        # print(f"이미지 태그 개수: {img_count}")

        top_blog_detail_dto.keyword = keyword
        top_blog_detail_dto.article_url = article_url
        top_blog_detail_dto.article_title = article_title
        top_blog_detail_dto.article_text = article_text
        top_blog_detail_dto.article_length = article_length
        top_blog_detail_dto.keyword_count = keyword_count
        # top_blog_detail_dto.img_count = img_count

        return top_blog_detail_dto


if __name__ == "__main__":
    bs = TistoryBeautifulsoup
    top_blog_detail_dto = bs.get_article_from_blog_url(
        bs,
        f"https://velog.io/@gywlsp/Medium-Velog-Tistory-%EA%B8%80-%ED%81%AC%EB%A1%A4%EB%A7%81-%EB%B0%A9%EB%B2%95",
        "크롤링",
    )
    top_blog_detail_dto.to_print()
