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

from threads.synonym_multiple_convert_thread import ConvertThread
from dtos.gui_dto import GUIDto


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

    def header_select_checkbox_changed(self):
        print(f"header: {self.header_select_checkbox.isChecked()}")
        if self.header_select_checkbox.isChecked():
            self.set_header_topic_combobox()
        else:
            self.header_topic_combobox.clear()

    def footer_select_checkbox_changed(self):
        print(f"footer: {self.footer_select_checkbox.isChecked()}")
        if self.footer_select_checkbox.isChecked():
            self.set_footer_topic_combobox()
        else:
            self.footer_topic_combobox.clear()

    def set_header_topic_combobox(self):
        self.saved_data_topic = get_save_data_topic()
        print(self.saved_data_topic)
        self.header_topic_combobox.clear()
        for i, topic in enumerate(self.saved_data_topic[SaveFileTopic.TOPIC.value]):
            self.header_topic_combobox.addItem(f"{topic}")

    def set_footer_topic_combobox(self):
        self.saved_data_topic = get_save_data_topic()
        print(self.saved_data_topic)
        self.footer_topic_combobox.clear()
        for i, topic in enumerate(self.saved_data_topic[SaveFileTopic.TOPIC.value]):
            self.footer_topic_combobox.addItem(f"{topic}")

    # 폴더 선택 클릭
    def convert_path_select_button_clicked(self):
        self.convert_listwidget.clear()
        self.convert_path.clear()
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder != "":
            self.convert_path.setText(folder)
            file_list = os.listdir(folder)
            print(file_list)
            for file in file_list:
                # 파일 형식을 지정합니다.
                if file.find("txt") > -1 or file.find("docx") > -1:
                    self.convert_listwidget.addItem(file)
        else:
            self.log_append(f"폴더 선택 취소")

    # 검색 시작 클릭
    def convert_start_button_clicked(self):
        print(f"search start clicked")

        # 유의어 변환 횟수
        if self.synonym_convert_limit.text() == "":
            QMessageBox.information(self, "작업 시작", f"유의어 변환 횟수를 입력해주세요.")
            return

        # 파일 목록
        selected_file_list = []
        self.convert_listwidget.selectAll()
        if len(self.convert_listwidget.selectedItems()) <= 0:
            print(f"선택된 파일이 없습니다.")
            QMessageBox.information(self, "작업 시작", f"선택된 파일이 없습니다.")
            return
        else:
            file_list_items = self.convert_listwidget.selectedItems()
            for file_item in file_list_items:
                selected_file_list.append(file_item.text())
        print(selected_file_list)

        # 엑셀 DB 확인
        self.saved_data_synonym = get_save_data_SYNONYM()
        if self.saved_data_synonym[SaveFileSYNONYM.SYNONYM_FILE_SAVE_PATH.value] == "":
            print(f"엑셀DB 파일을 설정해주세요.")
            # self.log_append(f"저장 경로를 먼저 설정해주세요.")
            QMessageBox.information(self, "작업 시작", f"엑셀DB 파일을 설정해주세요.")
            return
        else:
            search_file_save_path = self.saved_data_synonym[SaveFileSYNONYM.SYNONYM_FILE_SAVE_PATH.value]

        # 파일 유효성 검사
        if not os.path.isfile(search_file_save_path):
            QMessageBox.information(self, "작업 시작", f"엑셀 경로가 잘못되었습니다.")
            return

        # 양식에 맞는 엑셀파일인지 검증 필요
        try:
            synonym_file = SynonymFile(search_file_save_path)
            df_two_way: pd.DataFrame = synonym_file.df_two_way
            df_one_way: pd.DataFrame = synonym_file.df_one_way
        except Exception as e:
            print(e)
            QMessageBox.information(self, "작업 시작", f"양식에 맞지 않는 파일입니다. \n{e}")
            return

        # GUIDto
        guiDto = GUIDto()
        guiDto.synonym_convert_limit = self.synonym_convert_limit.text()
        guiDto.convert_path = self.convert_path.text()
        guiDto.convert_list = selected_file_list
        guiDto.shuffle_paragraphs_check = self.shuffle_paragraphs_checkbox.isChecked()
        guiDto.header_check = self.header_select_checkbox.isChecked()
        guiDto.header_topic = self.header_topic_combobox.currentText()
        guiDto.footer_check = self.footer_select_checkbox.isChecked()
        guiDto.footer_topic = self.footer_topic_combobox.currentText()
        guiDto.df_one_way = df_one_way
        guiDto.df_two_way = df_two_way
        guiDto.header_dict = get_save_data_HEADER()
        guiDto.footer_dict = get_save_data_FOOTER()

        print(f"작업을 시작합니다.")

        # 스레드 호출
        self.convert_thread = ConvertThread()
        self.convert_thread.log_msg.connect(self.log_append)
        self.convert_thread.convert_finished.connect(self.convert_finished)
        self.convert_thread.setGuiDto(guiDto)

        self.convert_start_button.setDisabled(True)
        self.convert_stop_button.setDisabled(False)
        self.convert_thread.start()

    # 검색 중지 클릭
    @pyqtSlot()
    def convert_stop_button_clicked(self):
        print(f"search stop clicked")
        self.log_append(f"중지 클릭")
        self.convert_finished()

    # 검색 작업 종료
    @pyqtSlot()
    def convert_finished(self):
        print(f"search thread finished")
        self.log_append(f"작업 종료")
        self.convert_thread.stop()
        self.convert_start_button.setDisabled(False)
        self.convert_stop_button.setDisabled(True)
        print(f"thread_is_running: {self.convert_thread.isRunning()}")

    def open_save_path_button_clicked(self):
        if self.convert_path.text() == "":
            QMessageBox.information(self, "폴더 열기", f"폴더를 먼저 설정해주세요.")
            return

        os.startfile(self.convert_path.text())

    # 메인 UI
    def initUI(self):
        # 유의어 변환 횟수
        synonym_convert_limit_groupbox = QGroupBox()
        self.synonym_convert_limit_label = QLabel("유의어 변환 횟수")
        self.synonym_convert_limit = QLineEdit()
        self.synonym_convert_limit.setValidator(QIntValidator())

        synonym_convert_limit_inner_layout = QHBoxLayout()
        synonym_convert_limit_inner_layout.addWidget(self.synonym_convert_limit_label)
        synonym_convert_limit_inner_layout.addWidget(self.synonym_convert_limit)
        synonym_convert_limit_groupbox.setLayout(synonym_convert_limit_inner_layout)

        # 변환할 폴더 선택
        convert_path_groupbox = QGroupBox()
        self.convert_path = QLineEdit()
        self.convert_path.setDisabled(True)
        self.convert_path_select_button = QPushButton("변환할 폴더 선택")

        self.convert_path_select_button.clicked.connect(self.convert_path_select_button_clicked)

        convert_path_inner_layout = QHBoxLayout()
        convert_path_inner_layout.addWidget(self.convert_path, 4)
        convert_path_inner_layout.addWidget(self.convert_path_select_button, 1)
        convert_path_groupbox.setLayout(convert_path_inner_layout)

        # 파일 목록 그룹박스
        convert_list_groupbox = QGroupBox("파일 목록")
        self.convert_listwidget = QListWidget(self)
        self.convert_listwidget.setSelectionMode(QAbstractItemView.MultiSelection)

        convert_list_inner_layout = QHBoxLayout()
        convert_list_inner_layout.addWidget(self.convert_listwidget)
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

        self.header_select_checkbox.stateChanged.connect(self.header_select_checkbox_changed)

        # 맺음말 삽입
        footer_select_groupbox = QGroupBox()
        self.footer_select_checkbox = QCheckBox("맺음말 삽입")
        self.footer_topic_combobox = QComboBox()

        footer_select_inner_layout = QHBoxLayout()
        footer_select_inner_layout.addWidget(self.footer_select_checkbox)
        footer_select_inner_layout.addWidget(self.footer_topic_combobox)
        footer_select_groupbox.setLayout(footer_select_inner_layout)

        self.footer_select_checkbox.stateChanged.connect(self.footer_select_checkbox_changed)

        # 변환 시작 중지 그룹박스
        convert_start_stop_groupbox = QGroupBox("변환하기")
        self.convert_start_button = QPushButton("시작")
        self.convert_stop_button = QPushButton("중지")
        self.convert_stop_button.setDisabled(True)
        self.convert_open_save_path_button = QPushButton("저장된 경로 열기")

        self.convert_start_button.clicked.connect(self.convert_start_button_clicked)
        self.convert_stop_button.clicked.connect(self.convert_stop_button_clicked)
        self.convert_open_save_path_button.clicked.connect(self.open_save_path_button_clicked)

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
        top_layout.addWidget(synonym_convert_limit_groupbox, 2)
        top_layout.addWidget(convert_path_groupbox, 3)

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
