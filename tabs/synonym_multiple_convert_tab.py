import sys
import warnings

warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import *

from common.utils import *
from config import *
from features.convert_sentence import convert_sentence
from common.synonym_file import SynonymFile
import pandas as pd
import clipboard
import random


class SynonymMultipleConvertTab(QWidget):
    # 초기화
    def __init__(self):
        super().__init__()
        self.initUI()

    # 로그 작성
    @pyqtSlot(str)
    def log_append(self, text):
        today = str(datetime.now())[0:10]
        now = str(datetime.now())[0:-7]
        self.browser.append(f"[{now}] {str(text)}")
        global_log_append(text)

    # 메인 UI
    def initUI(self):
        # 유의어 변환 횟수
        synonym_convert_limit_groupbox = QGroupBox("유의어 변환 횟수")
        synonym_convert_limit_inner_layout = QHBoxLayout()
        synonym_convert_limit_groupbox.setLayout(synonym_convert_limit_inner_layout)

        # 변환할 폴더 선택
        convert_path_groupbox = QGroupBox("변환할 폴더 선택")
        convert_path_inner_layout = QHBoxLayout()
        convert_path_groupbox.setLayout(convert_path_inner_layout)

        # 파일 목록 그룹박스
        convert_list_groupbox = QGroupBox("파일 목록")
        convert_list_inner_layout = QHBoxLayout()
        convert_list_groupbox.setLayout(convert_list_inner_layout)

        # 문단 랜덤 섞기
        shuffle_paragraphs_groupbox = QGroupBox()
        self.shuffle_paragraphs_checkbox = QCheckBox("문단 랜덤 섞기")

        shuffle_paragraphs_inner_layout = QHBoxLayout()
        shuffle_paragraphs_inner_layout.addWidget(self.shuffle_paragraphs_checkbox)
        shuffle_paragraphs_groupbox.setLayout(shuffle_paragraphs_inner_layout)

        # 머리글 삽입
        header_select_groupbox = QGroupBox()
        self.header_select_checkbox = QCheckBox("머리글 삽입")
        self.header_topic_combobox = QComboBox()

        header_select_inner_layout = QHBoxLayout()
        header_select_inner_layout.addWidget(self.header_select_checkbox)
        header_select_inner_layout.addWidget(self.header_topic_combobox)
        header_select_groupbox.setLayout(header_select_inner_layout)

        # self.header_select_checkbox.stateChanged.connect(self.header_select_checkbox_changed)

        # 맺음말 삽입
        footer_select_groupbox = QGroupBox()
        self.footer_select_checkbox = QCheckBox("맺음말 삽입")
        self.footer_topic_combobox = QComboBox()

        footer_select_inner_layout = QHBoxLayout()
        footer_select_inner_layout.addWidget(self.footer_select_checkbox)
        footer_select_inner_layout.addWidget(self.footer_topic_combobox)
        footer_select_groupbox.setLayout(footer_select_inner_layout)

        # self.footer_select_checkbox.stateChanged.connect(self.footer_select_checkbox_changed)

        # 변환 시작 중지 그룹박스
        convert_start_stop_groupbox = QGroupBox("변환하기")
        self.convert_start_button = QPushButton("시작")
        self.convert_stop_button = QPushButton("중지")
        self.convert_stop_button.setDisabled(True)
        self.convert_open_save_path_button = QPushButton("저장된 경로 열기")

        # self.convert_start_button.clicked.connect(self.convert_start_button_clicked)
        # self.convert_stop_button.clicked.connect(self.convert_stop_button_clicked)
        # self.convert_open_save_path_button.clicked.connect(self.convert_open_save_path_button_clicked)

        convert_start_stop_inner_layout = QHBoxLayout()
        convert_start_stop_inner_layout.addWidget(self.convert_start_button)
        convert_start_stop_inner_layout.addWidget(self.convert_stop_button)
        convert_start_stop_inner_layout.addWidget(self.convert_open_save_path_button)
        convert_start_stop_groupbox.setLayout(convert_start_stop_inner_layout)

        # 이미지 수집 시작 중지 그룹박스
        google_search_start_stop_groupbox = QGroupBox("이미지 수집 시작")
        self.google_search_start_button = QPushButton("시작")
        self.google_search_stop_button = QPushButton("중지")
        self.google_search_stop_button.setDisabled(True)
        self.open_save_path_button = QPushButton("저장된 경로 열기")

        # self.google_search_start_button.clicked.connect(self.google_search_start_button_clicked)
        # self.google_search_stop_button.clicked.connect(self.google_search_stop_button_clicked)
        # self.open_save_path_button.clicked.connect(self.open_save_path_button_clicked)

        google_search_start_stop_inner_layout = QHBoxLayout()
        google_search_start_stop_inner_layout.addWidget(self.google_search_start_button)
        google_search_start_stop_inner_layout.addWidget(self.google_search_stop_button)
        google_search_start_stop_inner_layout.addWidget(self.open_save_path_button)
        google_search_start_stop_groupbox.setLayout(google_search_start_stop_inner_layout)

        # 로그 그룹박스
        log_groupbox = QGroupBox("로그")
        self.browser = QTextBrowser()

        log_inner_layout = QHBoxLayout()
        log_inner_layout.addWidget(self.browser)
        log_groupbox.setLayout(log_inner_layout)

        # 레이아웃 배치
        top_layout = QHBoxLayout()
        top_layout.addWidget(synonym_convert_limit_groupbox)
        top_layout.addWidget(convert_path_groupbox)

        mid_layout = QHBoxLayout()
        mid_layout.addWidget(convert_list_groupbox)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(shuffle_paragraphs_groupbox)
        bottom_layout.addWidget(header_select_groupbox)
        bottom_layout.addWidget(footer_select_groupbox)

        lowest_layout = QHBoxLayout()
        lowest_layout.addWidget(convert_start_stop_groupbox)
        lowest_layout.addWidget(google_search_start_stop_groupbox)

        log_layout = QHBoxLayout()
        log_layout.addWidget(log_groupbox)

        left_layout = QVBoxLayout()
        left_layout.addLayout(top_layout)
        left_layout.addLayout(mid_layout)
        left_layout.addLayout(bottom_layout)
        left_layout.addLayout(lowest_layout)

        right_layout = QVBoxLayout()
        right_layout.addLayout(log_layout)

        layout = QHBoxLayout()
        layout.addLayout(left_layout, 3)
        layout.addLayout(right_layout, 2)

        self.setLayout(layout)
