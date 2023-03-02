import sys
import warnings

warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import *

from dtos.gui_dto import GUIDto
from threads.search_thread import SearchThread
from common.utils import *
from config import *
import collections


class SearchUI(QWidget):

    # 초기화
    def __init__(self):

        print(f"LOG_FOLDER_NAME: {LOG_FOLDER_NAME}")
        print(f"PROGRAM_PATH: {PROGRAM_PATH}")
        print(f"USER_SAVE_PATH_DAUM: {USER_SAVE_PATH_DAUM}")
        print(f"USER_SAVE_PATH_GOOGLE: {USER_SAVE_PATH_GOOGLE}")

        self.saved_data_daum = get_save_data_daum()
        self.saved_data_google = get_save_data_google()
        print(self.saved_data_daum)
        print(self.saved_data_google)

        super().__init__()
        self.initUI()

    # 로그 작성
    @pyqtSlot(str)
    def log_append(self, text):
        today = str(datetime.now())[0:10]
        now = str(datetime.now())[0:-7]
        self.browser.append(f"[{now}] {str(text)}")
        global_log_append(text)

    # 검색 시작 클릭
    def search_start_button_clicked(self):
        print(f"search start clicked")

        selected_daum_keyword_list = []
        self.daum_keyword_list_tablewidget.selectAll()
        daum_items = self.daum_keyword_list_tablewidget.selectedItems()
        if len(daum_items) <= 0:
            print(f"글 수집 키워드가 없습니다.")
            # self.log_append(f"글 수집 키워드가 없습니다.")
            QMessageBox.information(self, "작업 시작", f"글 수집 키워드가 없습니다.")
            return
        
        for daum_item in daum_items:
            row = daum_item.row()
            daum = QTableWidgetItem(self.daum_keyword_list_tablewidget.item(row, 0)).text()
            selected_daum_keyword_list.append(daum)

        selected_google_keyword_list = []
        self.google_keyword_list_tablewidget.selectAll()
        google_items = self.google_keyword_list_tablewidget.selectedItems()
        if len(google_items) <= 0:
            print(f"글 수집 키워드가 없습니다.")
            # self.log_append(f"글 수집 키워드가 없습니다.")
            QMessageBox.information(self, "작업 시작", f"글 수집 키워드가 없습니다.")
            return
        
        for google_item in google_items:
            row = google_item.row()
            google = QTableWidgetItem(self.google_keyword_list_tablewidget.item(row, 0)).text()
            selected_google_keyword_list.append(google)

        guiDto = GUIDto()
        guiDto.daum_keyword_list = selected_daum_keyword_list
        guiDto.google_keyword_list = selected_google_keyword_list

        print(f"{guiDto.daum_keyword_list} {guiDto.google_keyword_list} 작업을 시작합니다.")

        self.search_thread = SearchThread()
        self.search_thread.log_msg.connect(self.log_append)
        self.search_thread.search_finished.connect(self.search_finished)
        self.search_thread.setGuiDto(guiDto)

        self.search_start_button.setDisabled(True)
        self.search_stop_button.setDisabled(False)
        self.search_thread.start()

    # 검색 중지 클릭
    @pyqtSlot()
    def search_stop_button_clicked(self):
        print(f"search stop clicked")
        self.log_append(f"중지 클릭")
        self.search_finished()

    # 검색 작업 종료
    @pyqtSlot()
    def search_finished(self):
        print(f"search thread finished")
        self.log_append(f"작업 종료")
        self.search_thread.stop()
        self.search_start_button.setDisabled(False)
        self.search_stop_button.setDisabled(True)
        print(f"thread_is_running: {self.search_thread.isRunning()}")

    def set_daum_keyword_list_tablewidget(self):

        self.daum_keyword_list_tablewidget.setColumnCount(1)
        self.daum_keyword_list_tablewidget.setHorizontalHeaderLabels(["글 수집 키워드"])
        self.daum_keyword_list_tablewidget.setRowCount(len(self.saved_data_daum[SaveFileDaum.DAUM.value]))

        for i, keyword in enumerate(self.saved_data_daum[SaveFileDaum.DAUM.value]):
            self.daum_keyword_list_tablewidget.setItem(i, 0, QTableWidgetItem(keyword))

        self.daum_keyword_list_tablewidget.horizontalHeader().setSectionResizeMode(1)
        self.daum_keyword_list_tablewidget.setSelectionMode(QAbstractItemView.MultiSelection)

    def set_google_keyword_list_tablewidget(self):

        self.google_keyword_list_tablewidget.setColumnCount(1)
        self.google_keyword_list_tablewidget.setHorizontalHeaderLabels(["글 수집 키워드"])
        self.google_keyword_list_tablewidget.setRowCount(len(self.saved_data_google[SaveFileGoogle.GOOGLE.value]))

        for i, keyword in enumerate(self.saved_data_google[SaveFileGoogle.GOOGLE.value]):
            self.google_keyword_list_tablewidget.setItem(i, 0, QTableWidgetItem(keyword))

        self.google_keyword_list_tablewidget.horizontalHeader().setSectionResizeMode(1)
        self.google_keyword_list_tablewidget.setSelectionMode(QAbstractItemView.MultiSelection)

    def refresh_daum_button_clicked(self):
        self.refresh_save_file()
        self.set_daum_keyword_list_tablewidget()

    def refresh_google_button_clicked(self):
        self.refresh_save_file()
        self.set_google_keyword_list_tablewidget()

    def daum_save_button_clicked(self):

        if self.daum_input.text() == "":
            print(f"글 수집 키워드를 입력해주세요.")
            self.log_append(f"글 수집 키워드를 입력해주세요.")
            return

        keyword = self.daum_input.text()
        print(keyword)

        self.saved_data_daum[SaveFileDaum.DAUM.value].append(keyword)

        dict_save = {SaveFileDaum.DAUM.value: self.saved_data_daum[SaveFileDaum.DAUM.value]}

        write_save_data_daum(dict_save)

        self.refresh_save_file()

        self.set_daum_keyword_list_tablewidget()

    def google_save_button_clicked(self):

        if self.google_input.text() == "":
            print(f"이미지 수집 키워드를 입력해주세요.")
            self.log_append(f"이미지 수집 키워드를 입력해주세요.")
            return

        keyword = self.google_input.text()
        print(keyword)

        self.saved_data_google[SaveFileGoogle.GOOGLE.value].append(keyword)

        dict_save = {SaveFileGoogle.GOOGLE.value: self.saved_data_google[SaveFileGoogle.GOOGLE.value]}

        write_save_data_google(dict_save)

        self.refresh_save_file()

        self.set_google_keyword_list_tablewidget()

    def daum_remove_button_clicked(self):

        items = self.daum_keyword_list_tablewidget.selectedItems()
        if len(items) <= 0:
            print(f"선택된 글 수집 키워드가 없습니다.")
            # self.log_append(f"선택된 글 수집 키워드가 없습니다.")
            QMessageBox.information(self, "키워드 삭제", f"선택된 글 수집 키워드가 없습니다.")
            return

        question_msg = "선택된 항목을 삭제하시겠습니까?"
        reply = QMessageBox.question(self, "삭제", question_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:

            # 테이블에서 제거
            for item in items:
                row = item.row()
                self.daum_keyword_list_tablewidget.removeRow(row)

            try:
                # 메모장에 실 적용
                current_items = []
                for i in range(self.daum_keyword_list_tablewidget.rowCount()):
                    current_items.append(self.daum_keyword_list_tablewidget.item(i, 0).text())

                dict_save = {SaveFileDaum.DAUM.value: current_items}

                write_save_data_daum(dict_save)

                print(current_items)

                print(f"현재 상태를 저장했습니다.")
            except Exception as e:
                print(e)
        else:
            print(f"저장 취소")

        self.refresh_save_file()

        self.set_daum_keyword_list_tablewidget()

    def google_remove_button_clicked(self):

        items = self.google_keyword_list_tablewidget.selectedItems()
        if len(items) <= 0:
            print(f"선택된 이미지 수집 키워드가 없습니다.")
            # self.log_append(f"선택된 이미지 수집 키워드가 없습니다.")
            QMessageBox.information(self, "키워드 삭제", f"선택된 이미지 수집 키워드가 없습니다.")
            return

        question_msg = "선택된 항목을 삭제하시겠습니까?"
        reply = QMessageBox.question(self, "삭제", question_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:

            # 테이블에서 제거
            for item in items:
                row = item.row()
                self.google_keyword_list_tablewidget.removeRow(row)

            try:
                # 메모장에 실 적용
                current_items = []
                for i in range(self.google_keyword_list_tablewidget.rowCount()):
                    current_items.append(self.google_keyword_list_tablewidget.item(i, 0).text())

                dict_save = {SaveFileGoogle.GOOGLE.value: current_items}

                write_save_data_google(dict_save)

                print(current_items)

                print(f"현재 상태를 저장했습니다.")
            except Exception as e:
                print(e)
        else:
            print(f"저장 취소")

        self.refresh_save_file()

        self.set_google_keyword_list_tablewidget()

    def open_save_path_button_clicked(self):
        print("click")
        os.startfile(PROGRAM_PATH)

    # 저장파일 체크
    def refresh_save_file(self):
        self.saved_data_daum = get_save_data_daum()
        self.saved_data_google = get_save_data_google()
        print(self.saved_data_daum[SaveFileDaum.DAUM.value])
        print(self.saved_data_google[SaveFileGoogle.GOOGLE.value])

    # 메인 UI
    def initUI(self):

        # 다음 입력 그룹박스
        daum_input_groupbox = QGroupBox("글 수집 키워드")
        self.daum_input = QLineEdit()

        daum_input_inner_layout = QHBoxLayout()
        daum_input_inner_layout.addWidget(self.daum_input)

        daum_input_groupbox.setLayout(daum_input_inner_layout)

        # 다음 버튼 그룹박스
        daum_button_groupbox = QGroupBox("글 수집 키워드 추가")
        self.refresh_daum_button = QPushButton("목록 새로 고침")
        self.daum_save_button = QPushButton("키워드 추가")
        self.daum_remove_button = QPushButton("키워드 제거")

        self.refresh_daum_button.clicked.connect(self.refresh_daum_button_clicked)
        self.daum_save_button.clicked.connect(self.daum_save_button_clicked)
        self.daum_remove_button.clicked.connect(self.daum_remove_button_clicked)

        daum_button_inner_layout = QHBoxLayout()
        daum_button_inner_layout.addWidget(self.refresh_daum_button)
        daum_button_inner_layout.addWidget(self.daum_save_button)
        daum_button_inner_layout.addWidget(self.daum_remove_button)
        daum_button_groupbox.setLayout(daum_button_inner_layout)

        # 다음 목록 그룹박스
        daum_keyword_list_groupbox = QGroupBox("글 수집 키워드 목록")
        self.daum_keyword_list_tablewidget = QTableWidget()
        self.set_daum_keyword_list_tablewidget()

        daum_keyword_list_inner_layout = QVBoxLayout()
        daum_keyword_list_inner_layout.addWidget(self.daum_keyword_list_tablewidget)
        daum_keyword_list_groupbox.setLayout(daum_keyword_list_inner_layout)

        # 구글 입력 그룹박스
        google_input_groupbox = QGroupBox(f"이미지 수집 키워드")
        self.google_input = QLineEdit()

        google_input_inner_layout = QHBoxLayout()
        google_input_inner_layout.addWidget(self.google_input)
        google_input_groupbox.setLayout(google_input_inner_layout)

        # 구글 버튼 그룹박스
        google_button_groupbox = QGroupBox(f"이미지 수집 키워드 추가")
        self.refresh_google_button = QPushButton("목록 새로 고침")
        self.add_google_button = QPushButton("키워드 추가")
        self.remove_google_button = QPushButton("키워드 제거")

        self.refresh_google_button.clicked.connect(self.refresh_google_button_clicked)
        self.add_google_button.clicked.connect(self.google_save_button_clicked)
        self.remove_google_button.clicked.connect(self.google_remove_button_clicked)

        google_button_inner_layout = QHBoxLayout()
        google_button_inner_layout.addWidget(self.refresh_google_button)
        google_button_inner_layout.addWidget(self.add_google_button)
        google_button_inner_layout.addWidget(self.remove_google_button)
        google_button_groupbox.setLayout(google_button_inner_layout)

        # 구글 목록 그룹박스
        google_keyword_list_groupbox = QGroupBox("이미지 수집 키워드 목록")
        self.google_keyword_list_tablewidget = QTableWidget()
        self.set_google_keyword_list_tablewidget()

        google_keyword_list_inner_layout = QVBoxLayout()
        google_keyword_list_inner_layout.addWidget(self.google_keyword_list_tablewidget)
        google_keyword_list_groupbox.setLayout(google_keyword_list_inner_layout)

        # 수집할 페이지 수
        daum_page_setting_groupbox = QGroupBox("수집할 페이지 수")
        self.daum_start_page = QLineEdit()
        self.daum_start_page.setValidator(QIntValidator())
        self.daum_page_between = QLabel(" ~ ")
        self.daum_end_page = QLineEdit()
        self.daum_end_page.setValidator(QIntValidator())
        self.daum_page_range = QLabel(" 페이지 사이")

        daum_page_setting_inner_layout = QHBoxLayout()
        daum_page_setting_inner_layout.addWidget(self.daum_start_page)
        daum_page_setting_inner_layout.addWidget(self.daum_page_between)
        daum_page_setting_inner_layout.addWidget(self.daum_end_page)
        daum_page_setting_inner_layout.addWidget(self.daum_page_range)
        daum_page_setting_groupbox.setLayout(daum_page_setting_inner_layout)

        # 키워드별로 수집할 글 개수
        daum_search_count_groupbox = QGroupBox("키워드별로 수집할 글 개수")
        self.daum_search_count = QLineEdit()
        self.daum_search_count.setValidator(QIntValidator())
        self.daum_search_count_label = QLabel("개")

        daum_search_count_inner_layout = QHBoxLayout()
        daum_search_count_inner_layout.addWidget(self.daum_search_count)
        daum_search_count_inner_layout.addWidget(self.daum_search_count_label)
        daum_search_count_groupbox.setLayout(daum_search_count_inner_layout)

        # 수집할 글 작성일자 (이전에 작성된 글)
        daum_search_date_groupbox = QGroupBox("수집할 글 작성일자")
        self.daum_search_date = QDateEdit(QDate.currentDate())

        daum_search_date_inner_layout = QHBoxLayout()
        daum_search_date_inner_layout.addWidget(self.daum_search_date)
        daum_search_date_groupbox.setLayout(daum_search_date_inner_layout)

        # 키워드별로 수집할 이미지 개수
        google_search_count_groupbox = QGroupBox("키워드별로 수집할 이미지 개수")
        self.google_search_count = QLineEdit()
        self.google_search_count.setValidator(QIntValidator())
        self.google_search_count_label = QLabel("개")

        google_search_count_inner_layout = QHBoxLayout()
        google_search_count_inner_layout.addWidget(self.google_search_count)
        google_search_count_inner_layout.addWidget(self.google_search_count_label)
        google_search_count_groupbox.setLayout(google_search_count_inner_layout)

        # 시작 중지 그룹박스
        start_stop_groupbox = QGroupBox("작업 시작")
        self.search_start_button = QPushButton("시작")
        self.search_stop_button = QPushButton("중지")
        self.search_stop_button.setDisabled(True)
        self.open_save_path_button = QPushButton("저장된 경로 열기")

        self.search_start_button.clicked.connect(self.search_start_button_clicked)
        self.search_stop_button.clicked.connect(self.search_stop_button_clicked)
        self.open_save_path_button.clicked.connect(self.open_save_path_button_clicked)

        start_stop_inner_layout = QHBoxLayout()
        start_stop_inner_layout.addWidget(self.search_start_button)
        start_stop_inner_layout.addWidget(self.search_stop_button)
        start_stop_inner_layout.addWidget(self.open_save_path_button)
        start_stop_groupbox.setLayout(start_stop_inner_layout)

        # 로그 그룹박스
        log_groupbox = QGroupBox("로그")
        self.browser = QTextBrowser()

        log_inner_layout = QHBoxLayout()
        log_inner_layout.addWidget(self.browser)
        log_groupbox.setLayout(log_inner_layout)

        # 레이아웃 배치
        left_layout = QVBoxLayout()
        left_layout.addWidget(daum_input_groupbox)
        left_layout.addWidget(daum_button_groupbox)
        left_layout.addWidget(daum_keyword_list_groupbox)

        center_layout = QVBoxLayout()
        center_layout.addWidget(google_input_groupbox)
        center_layout.addWidget(google_button_groupbox)
        center_layout.addWidget(google_keyword_list_groupbox)

        right_layout = QVBoxLayout()
        right_layout.addWidget(daum_page_setting_groupbox)
        right_layout.addWidget(daum_search_count_groupbox)
        right_layout.addWidget(daum_search_date_groupbox)
        right_layout.addWidget(google_search_count_groupbox)
        right_layout.addWidget(start_stop_groupbox)
        right_layout.addWidget(log_groupbox)

        layout = QHBoxLayout()
        layout.addLayout(left_layout, 3)
        layout.addLayout(center_layout, 3)
        layout.addLayout(right_layout, 3)

        self.setLayout(layout)
