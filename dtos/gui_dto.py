class GUIDto:
    def __init__(self):
        # 검색
        self.__daum_keyword_list = []  # 다음 키워드
        self.__google_keyword_list = []  # 구글 키워드

        self.__daum_start_page = ""
        self.__daum_end_page = ""

        self.__daum_search_count = ""

        self.__daum_search_date = ""

        self.__google_search_count = ""

        self.__search_file_save_path = ""

        # 변환
        self.__synonym_convert_limit = ""

        self.__convert_path = ""

        self.__convert_list = []

        self.__shuffle_paragraphs_check = bool

        self.__header_check = bool

        self.__header_topic = ""

        self.__footer_check = bool

        self.__footer_topic = ""

        self.__header_dict = ""

        self.__footer_dict = ""

        self.__df_one_way = ""

        self.__df_two_way = ""

        # 파일 변환
        self.__convert_format = ""

        # 변환탭에서 이미지 수집
        self.__from_convert_tab = False

    @property
    def daum_keyword_list(self):  # getter
        return self.__daum_keyword_list

    @daum_keyword_list.setter
    def daum_keyword_list(self, value):  # setter
        self.__daum_keyword_list = value

    @property
    def google_keyword_list(self):  # getter
        return self.__google_keyword_list

    @google_keyword_list.setter
    def google_keyword_list(self, value):  # setter
        self.__google_keyword_list = value

    @property
    def daum_start_page(self):  # getter
        return self.__daum_start_page

    @daum_start_page.setter
    def daum_start_page(self, value):  # setter
        if value != "":
            value = int(value)
        self.__daum_start_page = value

    @property
    def daum_end_page(self):  # getter
        return self.__daum_end_page

    @daum_end_page.setter
    def daum_end_page(self, value):  # setter
        if value != "":
            value = int(value)
        self.__daum_end_page = value

    @property
    def daum_search_count(self):  # getter
        return self.__daum_search_count

    @daum_search_count.setter
    def daum_search_count(self, value):  # setter
        if value != "":
            value = int(value)
        self.__daum_search_count = value

    @property
    def daum_search_date(self):  # getter
        return self.__daum_search_date

    @daum_search_date.setter
    def daum_search_date(self, value):  # setter
        self.__daum_search_date = value

    @property
    def google_search_count(self):  # getter
        return self.__google_search_count

    @google_search_count.setter
    def google_search_count(self, value):  # setter
        if value != "":
            value = int(value)
        self.__google_search_count = value

    @property
    def search_file_save_path(self):  # getter
        return self.__search_file_save_path

    @search_file_save_path.setter
    def search_file_save_path(self, value):  # setter
        self.__search_file_save_path = value

    # 변환

    @property
    def synonym_convert_limit(self):  # getter
        return self.__synonym_convert_limit

    @synonym_convert_limit.setter
    def synonym_convert_limit(self, value):  # setter
        if value != "":
            value = int(value)
        self.__synonym_convert_limit = value

    @property
    def convert_path(self):  # getter
        return self.__convert_path

    @convert_path.setter
    def convert_path(self, value):  # setter
        self.__convert_path = value

    @property
    def convert_list(self):  # getter
        return self.__convert_list

    @convert_list.setter
    def convert_list(self, value):  # setter
        self.__convert_list = value

    @property
    def shuffle_paragraphs_check(self):  # getter
        return self.__shuffle_paragraphs_check

    @shuffle_paragraphs_check.setter
    def shuffle_paragraphs_check(self, value):  # setter
        self.__shuffle_paragraphs_check = value

    @property
    def header_check(self):  # getter
        return self.__header_check

    @header_check.setter
    def header_check(self, value):  # setter
        self.__header_check = value

    @property
    def header_topic(self):  # getter
        return self.__header_topic

    @header_topic.setter
    def header_topic(self, value):  # setter
        self.__header_topic = value

    @property
    def footer_check(self):  # getter
        return self.__footer_check

    @footer_check.setter
    def footer_check(self, value):  # setter
        self.__footer_check = value

    @property
    def footer_topic(self):  # getter
        return self.__footer_topic

    @footer_topic.setter
    def footer_topic(self, value):  # setter
        self.__footer_topic = value

    @property
    def header_dict(self):  # getter
        return self.__header_dict

    @header_dict.setter
    def header_dict(self, value):  # setter
        self.__header_dict = value

    @property
    def footer_dict(self):  # getter
        return self.__footer_dict

    @footer_dict.setter
    def footer_dict(self, value):  # setter
        self.__footer_dict = value

    @property
    def df_one_way(self):  # getter
        return self.__df_one_way

    @df_one_way.setter
    def df_one_way(self, value):  # setter
        self.__df_one_way = value

    @property
    def df_two_way(self):  # getter
        return self.__df_two_way

    @df_two_way.setter
    def df_two_way(self, value):  # setter
        self.__df_two_way = value

    # 파일 변환

    @property
    def convert_format(self):  # getter
        return self.__convert_format

    @convert_format.setter
    def convert_format(self, value):  # setter
        self.__convert_format = value

    @property
    def from_convert_tab(self):  # getter
        return self.__from_convert_tab

    @from_convert_tab.setter
    def from_convert_tab(self, value):  # setter
        self.__from_convert_tab = value
