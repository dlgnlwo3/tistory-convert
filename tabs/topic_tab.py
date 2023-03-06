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


class TopicUI(QWidget):

    # 초기화
    def __init__(self):

        self.saved_data_topic = get_save_data_topic()
        print(self.saved_data_topic)

        super().__init__()
        self.initUI()

    # 로그 작성
    @pyqtSlot(str)
    def log_append(self, text):
        today = str(datetime.now())[0:10]
        now = str(datetime.now())[0:-7]
        self.browser.append(f"[{now}] {str(text)}")
        global_log_append(text)

    def refresh_save_file(self):
        self.saved_data_topic = get_save_data_topic()
        print(self.saved_data_topic[SaveFileTopic.TOPIC.value])

    def refresh_topic_button_clicked(self):
        self.refresh_save_file()
        self.set_topic_list_tablewidget()

    def set_topic_list_tablewidget(self):

        self.topic_list_tablewidget.setColumnCount(1)
        self.topic_list_tablewidget.setHorizontalHeaderLabels(["주제"])
        self.topic_list_tablewidget.setRowCount(len(self.saved_data_topic[SaveFileTopic.TOPIC.value]))

        for i, keyword in enumerate(self.saved_data_topic[SaveFileTopic.TOPIC.value]):
            self.topic_list_tablewidget.setItem(i, 0, QTableWidgetItem(keyword))

        self.topic_list_tablewidget.horizontalHeader().setSectionResizeMode(1)
        self.topic_list_tablewidget.setSelectionMode(QAbstractItemView.MultiSelection)

    def topic_save_button_clicked(self):

        if self.topic_input.text() == "":
            print(f"주제를 입력해주세요.")
            QMessageBox.information(self, "주제 추가", f"주제를 입력해주세요.")
            # self.log_append(f"주제를 입력해주세요.")
            return

        keyword = self.topic_input.text()
        print(keyword)

        self.saved_data_topic[SaveFileTopic.TOPIC.value].append(keyword)

        dict_save = {SaveFileTopic.TOPIC.value: self.saved_data_topic[SaveFileTopic.TOPIC.value]}

        write_save_data_topic(dict_save)

        self.refresh_save_file()

        self.set_topic_list_tablewidget()

    def topic_remove_button_clicked(self):

        items = self.topic_list_tablewidget.selectedItems()
        if len(items) <= 0:
            print(f"선택된 주제가 없습니다.")
            # self.log_append(f"선택된 주제가 없습니다.")
            QMessageBox.information(self, "주제 삭제", f"선택된 주제가 없습니다.")
            return

        question_msg = "선택된 항목을 삭제하시겠습니까?"
        reply = QMessageBox.question(self, "삭제", question_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:

            # 테이블에서 제거
            for item in items:
                row = item.row()
                self.topic_list_tablewidget.removeRow(row)

            try:
                # 메모장에 실 적용
                current_items = []
                for i in range(self.topic_list_tablewidget.rowCount()):
                    current_items.append(self.topic_list_tablewidget.item(i, 0).text())

                dict_save = {SaveFileTopic.TOPIC.value: current_items}

                write_save_data_topic(dict_save)

                print(current_items)

                print(f"현재 상태를 저장했습니다.")
            except Exception as e:
                print(e)
        else:
            print(f"저장 취소")

        self.refresh_save_file()

        self.set_topic_list_tablewidget()

    # 메인 UI
    def initUI(self):

        # 주제 관리
        topic_groupbox = QGroupBox("주제 관리")
        self.topic_input_label = QLabel("주제 관리")
        self.topic_input = QLineEdit()
        self.topic_save_button = QPushButton("저장")
        self.topic_remove_button = QPushButton("제거")
        self.topic_list_tablewidget = QTableWidget()
        self.set_topic_list_tablewidget()

        self.topic_save_button.clicked.connect(self.topic_save_button_clicked)
        self.topic_remove_button.clicked.connect(self.topic_remove_button_clicked)

        topic_inner_layout = QGridLayout()
        topic_inner_layout.addWidget(self.topic_input_label, 0, 0, 1, 1)
        topic_inner_layout.addWidget(self.topic_input, 0, 1, 1, 1)
        topic_inner_layout.addWidget(self.topic_save_button, 0, 2, 1, 1)
        topic_inner_layout.addWidget(self.topic_remove_button, 0, 3, 1, 1)
        topic_inner_layout.addWidget(self.topic_list_tablewidget, 1, 1, 2, 1)
        topic_groupbox.setLayout(topic_inner_layout)

        # 로그 그룹박스
        log_groupbox = QGroupBox("로그")
        self.browser = QTextBrowser()

        log_inner_layout = QHBoxLayout()
        log_inner_layout.addWidget(self.browser)
        log_groupbox.setLayout(log_inner_layout)

        # 레이아웃 배치
        top_layout = QVBoxLayout()
        top_layout.addWidget(topic_groupbox)

        mid_layout = QHBoxLayout()

        log_layout = QVBoxLayout()
        log_layout.addWidget(log_groupbox)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addLayout(mid_layout)
        layout.addLayout(log_layout)

        self.setLayout(layout)
