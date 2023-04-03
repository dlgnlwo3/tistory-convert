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

from dtos.gui_dto import GUIDto

from threads.file_convert_thread import FileConvertThread
from playsound import playsound


class FileConvertTab(QWidget):
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
                if self.txt_to_docx.isChecked():
                    if file.find("txt") > -1:
                        self.convert_listwidget.addItem(file)

                elif self.docx_to_txt.isChecked():
                    if file.find("docx") > -1:
                        self.convert_listwidget.addItem(file)

        else:
            self.log_append(f"폴더 선택 취소")

    def radio_button_toggled(self):
        self.convert_path.clear()
        self.convert_listwidget.clear()

    def open_save_path_button_clicked(self):
        if self.convert_path.text() == "":
            QMessageBox.information(self, "폴더 열기", f"폴더를 먼저 설정해주세요.")
            return

        os.startfile(self.convert_path.text())

    def convert_start_button_clicked(self):
        print(f"search start clicked")

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

        # 체크된 라디오 버튼
        if self.docx_to_txt.isChecked():
            print("txt")
            convert_format = "txt"

        elif self.txt_to_docx.isChecked():
            print("docx")
            convert_format = "docx"

        # GUIDto
        guiDto = GUIDto()
        guiDto.convert_list = selected_file_list
        guiDto.convert_format = convert_format
        guiDto.convert_path = self.convert_path.text()

        print(f"작업을 시작합니다.")

        # 스레드 호출
        self.convert_thread = FileConvertThread()
        self.convert_thread.log_msg.connect(self.log_append)
        self.convert_thread.convert_finished.connect(self.convert_finished)
        self.convert_thread.setGuiDto(guiDto)

        self.convert_start_button.setDisabled(True)
        self.convert_stop_button.setDisabled(False)
        self.convert_thread.start()

    @pyqtSlot()
    def convert_stop_button_clicked(self):
        print(f"search stop clicked")
        self.log_append(f"중지 클릭")
        self.convert_finished()

    @pyqtSlot()
    def convert_finished(self):
        print(f"search thread finished")
        self.log_append(f"작업 종료")
        self.convert_thread.stop()
        self.convert_start_button.setDisabled(False)
        self.convert_stop_button.setDisabled(True)
        print(f"thread_is_running: {self.convert_thread.isRunning()}")
        if self.system_sound_checkbox.isChecked():
            print("알림음")
            playsound(r"D:\Consolework\tistory-convert-new\assets\thread_finished_sound.mp3")

    # 메인 UI
    def initUI(self):
        # 텍스트파일 -> 워드파일, 워드파일 -> 텍스트파일
        convert_radio_button_groupbox = QGroupBox()
        self.txt_to_docx = QRadioButton("텍스트 파일 -> 워드 파일")
        self.txt_to_docx.setChecked(True)
        self.docx_to_txt = QRadioButton("워드 파일 -> 텍스트 파일")

        self.txt_to_docx.toggled.connect(self.radio_button_toggled)
        self.docx_to_txt.toggled.connect(self.radio_button_toggled)

        convert_radio_button_inner_layout = QHBoxLayout()
        convert_radio_button_inner_layout.addWidget(self.txt_to_docx)
        convert_radio_button_inner_layout.addWidget(self.docx_to_txt)
        convert_radio_button_groupbox.setLayout(convert_radio_button_inner_layout)

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

        # 작업 완료 시 작동하는 그룹박스
        system_down_groupbox = QGroupBox("작업 완료 시 설정")
        self.system_sound_checkbox = QCheckBox("작업 완료 시 알림")

        system_down_inner_layout = QHBoxLayout()
        system_down_inner_layout.addWidget(self.system_sound_checkbox)
        system_down_groupbox.setLayout(system_down_inner_layout)

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

        # 로그 그룹박스
        log_groupbox = QGroupBox("로그")
        self.browser = QTextBrowser()

        log_inner_layout = QHBoxLayout()
        log_inner_layout.addWidget(self.browser)
        log_groupbox.setLayout(log_inner_layout)

        # 레이아웃 배치
        top_layout = QHBoxLayout()
        top_layout.addWidget(convert_radio_button_groupbox, 2)
        top_layout.addWidget(convert_path_groupbox, 3)

        mid_layout = QHBoxLayout()
        mid_layout.addWidget(convert_list_groupbox)

        bottom_layout = QHBoxLayout()

        lowest_layout = QHBoxLayout()
        lowest_layout.addWidget(system_down_groupbox)
        lowest_layout.addWidget(convert_start_stop_groupbox)

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
