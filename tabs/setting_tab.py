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


class SettingUI(QWidget):

    # 초기화
    def __init__(self):

        self.saved_data = get_save_data_setting()
        print(self.saved_data)

        super().__init__()
        self.initUI()

    # 로그 작성
    @pyqtSlot(str)
    def log_append(self, text):
        today = str(datetime.now())[0:10]
        now = str(datetime.now())[0:-7]
        self.browser.append(f"[{now}] {str(text)}")
        global_log_append(text)

    # 상태 저장
    def search_file_save_path_save_button_clicked(self):

        search_file_save_path = self.search_file_save_path.text()

        dict_save = {
            SaveFileSetting.SEARCH_FILE_SAVE_PATH.value: search_file_save_path,
        }

        question_msg = "저장하시겠습니까?"
        reply = QMessageBox.question(self, "상태 저장", question_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            write_save_data_setting(dict_save)
            print(f"현재 상태를 저장했습니다.")
        else:
            print(f"저장 취소")

    # 이미지 경로 선택
    def search_file_save_path_select_button_clicked(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder != "":
            self.search_file_save_path.setText(folder)
        else:
            self.log_append(f"선택된 폴더가 없습니다.")

    # 메인 UI
    def initUI(self):

        # 수집 파일 저장 경로
        search_file_save_path_groupbox = QGroupBox("수집 파일 저장 경로")
        self.search_file_save_path = QLineEdit(f"{self.saved_data[SaveFileSetting.SEARCH_FILE_SAVE_PATH.value]}")
        self.search_file_save_path.setDisabled(True)
        self.search_file_save_path_select_button = QPushButton("폴더 선택")
        self.search_file_save_path_save_button = QPushButton("저장")

        self.search_file_save_path_select_button.clicked.connect(self.search_file_save_path_select_button_clicked)
        self.search_file_save_path_save_button.clicked.connect(self.search_file_save_path_save_button_clicked)

        search_file_save_path_inner_layout = QHBoxLayout()
        search_file_save_path_inner_layout.addWidget(self.search_file_save_path)
        search_file_save_path_inner_layout.addWidget(self.search_file_save_path_select_button)
        search_file_save_path_inner_layout.addWidget(self.search_file_save_path_save_button)
        search_file_save_path_groupbox.setLayout(search_file_save_path_inner_layout)

        # 로그 그룹박스
        log_groupbox = QGroupBox("로그")
        self.browser = QTextBrowser()

        log_inner_layout = QHBoxLayout()
        log_inner_layout.addWidget(self.browser)
        log_groupbox.setLayout(log_inner_layout)

        # 레이아웃 배치
        top_layout = QVBoxLayout()
        top_layout.addWidget(search_file_save_path_groupbox)

        mid_layout = QHBoxLayout()

        log_layout = QVBoxLayout()
        log_layout.addWidget(log_groupbox)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addLayout(mid_layout)
        layout.addLayout(log_layout)

        self.setLayout(layout)
