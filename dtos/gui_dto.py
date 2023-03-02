class GUIDto:
    def __init__(self):

        self.__daum_keyword_list = []  # 다음 키워드
        self.__google_keyword_list = []  # 구글 키워드

        self.__daum_start_page = ""
        self.__daum_end_page = ""

        self.__daum_search_count = ''

        self.__daum_search_date = ''

        self.__google_search_count = ''

    @property
    def daum_keyword_list(self):  # getter
        return self.__daum_keyword_list

    @daum_keyword_list.setter
    def daum_keyword_list(self, value: list):  # setter
        self.__daum_keyword_list = value

    @property
    def google_keyword_list(self):  # getter
        return self.__google_keyword_list

    @google_keyword_list.setter
    def google_keyword_list(self, value: list):  # setter
        self.__google_keyword_list = value

    @property
    def daum_start_page(self):  # getter
        return self.__daum_start_page

    @daum_start_page.setter
    def daum_start_page(self, value: list):  # setter
        self.__daum_start_page = value

    @property
    def daum_end_page(self):  # getter
        return self.__daum_end_page

    @daum_end_page.setter
    def daum_end_page(self, value: list):  # setter
        self.__daum_end_page = value

    @property
    def daum_search_count(self):  # getter
        return self.__daum_search_count

    @daum_search_count.setter
    def daum_search_count(self, value: list):  # setter
        self.__daum_search_count = value

    @property
    def daum_search_date(self):  # getter
        return self.__daum_search_date

    @daum_search_date.setter
    def daum_search_date(self, value: list):  # setter
        self.__daum_search_date = value

    @property
    def google_search_count(self):  # getter
        return self.__google_search_count

    @google_search_count.setter
    def google_search_count(self, value: list):  # setter
        self.__google_search_count = value