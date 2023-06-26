if 1 == 1:
    import sys
    import warnings
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    warnings.simplefilter("ignore", UserWarning)
    sys.coinit_flags = 2

import os
from dtos.top_blog_detail_dto import *
from common.utils import convert_multiple_newlines
from bs4 import BeautifulSoup
import requests


class TistoryBeautifulSoup:
    def __init__(self):
        pass

    # 입력받은 url에서 이미지태그 개수와 키워드 반복횟수를 파악합니다.
    def get_detail_info(self, blog_url: str):
        article_text = ""
        article_title = ""
        img_count = 0
        article_url = ""

        response = requests.get(blog_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove text within the <a> tags
        for a in soup.find_all("a"):
            a.decompose()

        # img_tags = soup.find_all('img')

        # for img in img_tags:
        #     alt_text = img.get('alt')
        #     alt_text.decompose()  # Remove the img tag from the HTML
        # Perform any desired processing or queries with the alt_text

        for mark in soup.find_all("div", {"class": "mark"}):
            mark.decompose()

        for figcaption in soup.find_all("figcaption"):
            figcaption.decompose()

        try:
            article_title = soup.select_one(".blogview_tit h3").get_text()
        except:
            pass

        content_img_els = soup.select("article img")
        content_img_list = [
            content_img
            for content_img in content_img_els
            if not any(
                keyword in content_img["src"]
                for keyword in ["/thumb/", "daumcdn.net/map", "googlesyndication.com", "https://adclick"]
            )
        ]
        img_count = str(len(content_img_list))
        article_url = response.url

        try:
            div_soup = soup.find("div", class_="useless_p_margin")
        except:
            pass

        if not div_soup:
            try:
                div_soup = soup.find("div", class_="blogview_content")
            except:
                pass

        if not div_soup:
            try:
                div_soup = soup.find("div", class_="tt_article_useless_p_margin")
            except:
                pass

        if not div_soup:
            raise Exception("본문을 찾을 수 없습니다.")

        # Find the ul and li tags
        ul_tags = div_soup.find_all("ul")

        for ul_tag in ul_tags:
            li_tags = ul_tag.find_all("li")
            for li_tag in li_tags:
                br_tags = li_tag.find_all("br")
                for br_tag in br_tags:
                    br_tag.replace_with("\n")
                li_tag.insert_after(soup.new_string("\n"))

        article_text = div_soup.get_text()

        # 줄바꿈 수정 3개이상인경우 2개로 수정
        article_text = convert_multiple_newlines(article_text)

        return article_title, article_text, article_url, img_count

    # 입력받은 url에서 이미지태그 개수와 키워드 반복횟수를 파악합니다.
    def get_article_detail(self, blog_url: str, keyword: str):
        if blog_url.find(".com") > -1 and blog_url.find(".com/m/") == -1:
            blog_url = blog_url.replace(".com/", ".com/m/")
        elif blog_url.find(".org") > -1 and blog_url.find(".org/m/") == -1:
            blog_url = blog_url.replace(".org/", ".org/m/")
        elif blog_url.find(".kr") > -1 and blog_url.find(".kr/m/") == -1:
            blog_url = blog_url.replace(".kr/", ".kr/m/")
        elif blog_url.find(".net") > -1 and blog_url.find(".net/m/") == -1:
            blog_url = blog_url.replace(".net/", ".net/m/")

        top_blog_detail_dto = TopBlogDetailDto()

        article_title, article_text, article_url, img_count = self.get_detail_info(blog_url)
        if not article_title:
            article_title = keyword

        article_text = str(article_text)
        article_length = len(article_text.replace("\xa0", "").replace(" ", "").replace(f"\n", ""))
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
    # blog_url = f"https://sj.donnhyeokarea.com/49"
    # keyword = "사과 효능"

    # 불렛포인트 줄바꿈오류 수정
    # blog_url = f"https://wlrmtwlrmt.againnew.co.kr/16"
    # keyword = "불렛포인트"

    # blog_url = f"https://moneyalarms.com/51"
    # blog_url = f"https://rinte.net/866"
    # keyword = "참외 효능 부작용"

    # blog_url = f"https://fff.98hee.com/86"
    # keyword = "참외 효능 부작용"

    blog_url = f"https://wlrmtwlrmt.againnew.co.kr/16"
    keyword = "사과고르는법"

    newspaper = TistoryBeautifulSoup()
    topBlogDetailDto = newspaper.get_article_detail(blog_url, keyword)
    topBlogDetailDto.to_print()
