class TopBlogDetailDto:

    # keyword, article_url, article_title, article_text, keyword_count, len(img_tags)

    def __init__(self):
        self.__keyword = ""
        self.__article_url = ""
        self.__article_title = ""
        self.__article_text = ""
        self.__keyword_count = ""
        self.__img_count = ""

    @property
    def keyword(self):  # getter
        return self.__keyword

    @keyword.setter
    def keyword(self, value: str):  # setter
        self.__keyword = value

    @property
    def article_url(self):  # getter
        return self.__article_url

    @article_url.setter
    def article_url(self, value: str):  # setter
        self.__article_url = value

    @property
    def article_title(self):  # getter
        return self.__article_title

    @article_title.setter
    def article_title(self, value: str):  # setter
        self.__article_title = value

    @property
    def article_text(self):  # getter
        return self.__article_text

    @article_text.setter
    def article_text(self, value: str):  # setter
        self.__article_text = value

    @property
    def keyword_count(self):  # getter
        return self.__keyword_count

    @keyword_count.setter
    def keyword_count(self, value):  # setter
        self.__keyword_count = value

    @property
    def img_count(self):  # getter
        return self.__img_count

    @img_count.setter
    def img_count(self, value):  # setter
        self.__img_count = value

    def to_print(self):
        print("keyword", self.keyword)
        print("article_url", self.article_url)
        print("article_title", self.article_title)
        print("article_text", self.article_text)
        print("keyword_count", self.keyword_count)
        print("img_count", self.img_count)

    def get_dict(self) -> dict:
        return {
            "키워드": self.keyword,
            "url": self.article_url,
            "제목": self.article_title,
            "내용": self.article_text,
            "키워드반복횟수": self.keyword_count,
            "이미지개수": self.img_count,
        }
