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

        self.saved_data_setting = get_save_data_setting()
        print(self.saved_data_setting)

        self.saved_data_synonym = get_save_data_SYNONYM()
        print(self.saved_data_synonym)

        super().__init__()
        self.initUI()

    # 로그 작성
    @pyqtSlot(str)
    def log_append(self, text):
        today = str(datetime.now())[0:10]
        now = str(datetime.now())[0:-7]
        self.browser.append(f"[{now}] {str(text)}")
        global_log_append(text)

    # 이미지 경로 선택
    def search_file_save_path_select_button_clicked(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder != "":
            self.search_file_save_path.setText(folder)
        else:
            self.log_append(f"선택된 폴더가 없습니다.")

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
            QMessageBox.information(self, "경로 저장", f"수집 파일 저장 경로를 저장했습니다.")
            print(f"수집 파일 저장 경로를 저장했습니다.")
        else:
            print(f"저장 취소")

    def synonym_file_select_button_clicked(self):
        print(f"excel file select")
        file_name = QFileDialog.getOpenFileName(self, "", "", "excel file (*.xlsx)")

        if file_name[0] == "":
            print(f"선택된 파일이 없습니다.")
            return

        print(file_name[0])
        self.synonym_file.setText(file_name[0])

    def synonym_file_save_button_clicked(self):
        synonym_file_save_path = self.synonym_file.text()

        dict_save = {
            SaveFileSYNONYM.SYNONYM_FILE_SAVE_PATH.value: synonym_file_save_path,
        }

        question_msg = "저장하시겠습니까?"
        reply = QMessageBox.question(self, "상태 저장", question_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            write_save_data_SYNONYM(dict_save)
            QMessageBox.information(self, "파일 저장", f"유의어 엑셀 DB를 저장했습니다.")
            print(f"유의어 엑셀 DB를 저장했습니다.")
        else:
            print(f"저장 취소")

    # 메인 UI
    def initUI(self):

        # 수집 파일 저장 경로
        search_file_save_path_groupbox = QGroupBox("수집 파일 저장 경로")
        self.search_file_save_path = QLineEdit(
            f"{self.saved_data_setting[SaveFileSetting.SEARCH_FILE_SAVE_PATH.value]}"
        )
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

        # 유의어 엑셀 DB 불러오기
        synonym_file_groupbox = QGroupBox("유의어 엑셀 DB 불러오기")
        self.synonym_file = QLineEdit(f"{self.saved_data_synonym[SaveFileSYNONYM.SYNONYM_FILE_SAVE_PATH.value]}")
        self.synonym_file.setDisabled(True)
        self.synonym_file_select_button = QPushButton("파일 선택")
        self.synonym_file_save_button = QPushButton("저장")

        self.synonym_file_select_button.clicked.connect(self.synonym_file_select_button_clicked)
        self.synonym_file_save_button.clicked.connect(self.synonym_file_save_button_clicked)

        synonym_file_inner_layout = QHBoxLayout()
        synonym_file_inner_layout.addWidget(self.synonym_file)
        synonym_file_inner_layout.addWidget(self.synonym_file_select_button)
        synonym_file_inner_layout.addWidget(self.synonym_file_save_button)
        synonym_file_groupbox.setLayout(synonym_file_inner_layout)

        # 레이아웃 배치
        top_layout = QHBoxLayout()
        top_layout.addStretch(1)
        top_layout.addWidget(search_file_save_path_groupbox, 7)
        top_layout.addStretch(1)

        mid_layout = QHBoxLayout()
        mid_layout.addStretch(1)
        mid_layout.addWidget(synonym_file_groupbox, 7)
        mid_layout.addStretch(1)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch(1)
        bottom_layout.addStretch(1)

        layout = QVBoxLayout()
        layout.addLayout(top_layout, 1)
        layout.addLayout(mid_layout, 1)
        layout.addLayout(bottom_layout, 1)
        layout.addStretch(8)

        self.setLayout(layout)
