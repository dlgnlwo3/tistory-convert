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
from bs4 import BeautifulSoup
import requests


class TistoryBeautifulsoup:
    def __init__(self):
        pass

    def get_article_from_blog_url(self, blog_url: str, keyword: str):
        top_blog_detail_dto = TopBlogDetailDto()

        if blog_url.find(".com") > -1 and blog_url.find(".com/m/") == -1:
            blog_url = blog_url.replace(".com/", ".com/m/")
        elif blog_url.find(".org") > -1 and blog_url.find(".org/m/") == -1:
            blog_url = blog_url.replace(".org/", ".org/m/")
        elif blog_url.find(".kr") > -1 and blog_url.find(".kr/m/") == -1:
            blog_url = blog_url.replace(".kr/", ".kr/m/")

        response = requests.get(blog_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        article_text = ""

        # 본문 내용 추출
        # document.querySelector('.tt_article_useless_p_margin')
        try:
            div_soup = soup.find("div", class_="useless_p_margin")
            article_url = response.url
            article_text = div_soup.text
        except:
            pass
        
        if not article_text:
            try:
                div_soup = soup.find("div", class_="blogview_content")
                article_url = response.url
                article_text = div_soup.text
            except:
                pass
        
        if not article_text:
            try:
                div_soup = soup.find("div", class_="tt_article_useless_p_margin")
                article_url = response.url
                article_text = div_soup.text
            except:
                pass

        if not article_text:
            raise Exception("본문을 찾을 수 없습니다.")


        article_url = response.url
        article_title = '제목부분'
        article_text = div_soup.text

        article_length = len(article_text)

        keyword_count = article_text.count(keyword)

        clipboard.copy(str(article_text))

        top_blog_detail_dto.keyword = keyword
        top_blog_detail_dto.article_url = article_url
        top_blog_detail_dto.article_title = article_title
        top_blog_detail_dto.article_text = article_text
        top_blog_detail_dto.article_length = article_length
        top_blog_detail_dto.keyword_count = keyword_count

        return top_blog_detail_dto


if __name__ == "__main__":

    # blog_url = f"https://ruha007.tistory.com/95"
    blog_url = f"http://happyeasybaking.tistory.com/106"
    keyword = "변비"

    bs4 = TistoryBeautifulsoup()
    topBlogDetailDto = bs4.get_article_from_blog_url(blog_url, keyword)
    topBlogDetailDto.to_print()
    
