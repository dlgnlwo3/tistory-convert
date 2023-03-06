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

        self.saved_data_header = get_save_data_HEADER()
        print(self.saved_data_header)

        self.saved_data_footer = get_save_data_FOOTER()
        print(self.saved_data_footer)

        super().__init__()
        self.initUI()

    def refresh_save_file(self):
        self.saved_data_topic = get_save_data_topic()
        print(self.saved_data_topic)
        self.saved_data_header = get_save_data_HEADER()
        print(self.saved_data_header)
        self.saved_data_footer = get_save_data_FOOTER()
        print(self.saved_data_footer)

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

        topic = self.topic_input.text()
        print(topic)

        self.saved_data_topic[SaveFileTopic.TOPIC.value].append(topic)

        dict_save = {SaveFileTopic.TOPIC.value: self.saved_data_topic[SaveFileTopic.TOPIC.value]}

        write_save_data_topic(dict_save)

        self.refresh_save_file()

        self.set_topic_list_tablewidget()

        self.set_combobox()

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

                print(dict_save)

                print(f"현재 상태를 저장했습니다.")
            except Exception as e:
                print(e)
        else:
            print(f"저장 취소")

        self.refresh_save_file()

        self.set_topic_list_tablewidget()

        self.set_combobox()

    # 콤보박스 세팅
    def set_combobox(self):

        self.header_topic_combobox.clear()
        self.footer_topic_combobox.clear()

        for i, topic in enumerate(self.saved_data_topic[SaveFileTopic.TOPIC.value]):
            self.header_topic_combobox.addItem(f"{topic}")
            self.footer_topic_combobox.addItem(f"{topic}")

    def header_save_button_clicked(self):

        if self.header_input.text() == "":
            QMessageBox.information(self, "머리글 저장", f"머리글을 입력해주세요.")
            return

        try:
            saved_topic_header = self.saved_data_header[self.header_topic_combobox.currentText()]

        except Exception as e:
            saved_topic_header = []

        saved_topic_header.append(self.header_input.text())

        save_topic_header = {self.header_topic_combobox.currentText(): saved_topic_header}

        self.saved_data_header.update(save_topic_header)

        dict_save = self.saved_data_header

        write_save_data_HEADER(dict_save)

        self.refresh_save_file()

        self.set_header_list_tablewidget()

    def footer_save_button_clicked(self):

        if self.footer_input.text() == "":
            QMessageBox.information(self, "맺음말 저장", f"맺음말을 입력해주세요.")
            return

        try:
            saved_topic_footer = self.saved_data_footer[self.footer_topic_combobox.currentText()]

        except Exception as e:
            saved_topic_footer = []

        saved_topic_footer.append(self.footer_input.text())

        save_topic_footer = {self.footer_topic_combobox.currentText(): saved_topic_footer}

        self.saved_data_footer.update(save_topic_footer)

        dict_save = self.saved_data_footer

        write_save_data_FOOTER(dict_save)

        self.refresh_save_file()

        self.set_footer_list_tablewidget()

    def header_remove_button_clicked(self):

        items = self.header_list_tablewidget.selectedItems()
        if len(items) <= 0:
            print(f"선택된 머리글이 없습니다.")
            QMessageBox.information(self, "머리글 삭제", f"선택된 머리글이 없습니다.")
            return

        question_msg = "선택된 항목을 삭제하시겠습니까?"
        reply = QMessageBox.question(self, "삭제", question_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:

            # 테이블에서 제거
            for item in items:
                row = item.row()
                self.header_list_tablewidget.removeRow(row)

            try:
                # 메모장에 실 적용
                current_items = []
                for i in range(self.header_list_tablewidget.rowCount()):
                    current_items.append(self.header_list_tablewidget.item(i, 0).text())

                try:
                    saved_topic_header = self.saved_data_header[self.header_topic_combobox.currentText()]

                except Exception as e:
                    saved_topic_header = []

                self.saved_data_header.update({self.header_topic_combobox.currentText(): current_items})

                dict_save = self.saved_data_header

                write_save_data_HEADER(dict_save)

                print(current_items)

                print(f"현재 상태를 저장했습니다.")

            except Exception as e:
                print(e)

        else:
            print(f"저장 취소")

        self.refresh_save_file()

        self.set_header_list_tablewidget()

    def footer_remove_button_clicked(self):

        items = self.footer_list_tablewidget.selectedItems()
        if len(items) <= 0:
            print(f"선택된 머리글이 없습니다.")
            QMessageBox.information(self, "머리글 삭제", f"선택된 머리글이 없습니다.")
            return

        question_msg = "선택된 항목을 삭제하시겠습니까?"
        reply = QMessageBox.question(self, "삭제", question_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:

            # 테이블에서 제거
            for item in items:
                row = item.row()
                self.footer_list_tablewidget.removeRow(row)

            try:
                # 메모장에 실 적용
                current_items = []
                for i in range(self.footer_list_tablewidget.rowCount()):
                    current_items.append(self.footer_list_tablewidget.item(i, 0).text())

                try:
                    saved_topic_footer = self.saved_data_footer[self.footer_topic_combobox.currentText()]

                except Exception as e:
                    saved_topic_footer = []

                self.saved_data_footer.update({self.footer_topic_combobox.currentText(): current_items})

                dict_save = self.saved_data_footer

                write_save_data_FOOTER(dict_save)

                print(current_items)

                print(f"현재 상태를 저장했습니다.")

            except Exception as e:
                print(e)

        else:
            print(f"저장 취소")

        self.refresh_save_file()

        self.set_footer_list_tablewidget()

    def set_header_list_tablewidget(self):

        self.header_list_tablewidget.setColumnCount(1)
        self.header_list_tablewidget.setHorizontalHeaderLabels(["머리글"])

        try:
            self.header_list_tablewidget.setRowCount(
                len(self.saved_data_header[self.header_topic_combobox.currentText()])
            )
            for i, header in enumerate(self.saved_data_header[self.header_topic_combobox.currentText()]):
                self.header_list_tablewidget.setItem(i, 0, QTableWidgetItem(header))
        except Exception as e:
            pass

        self.header_list_tablewidget.horizontalHeader().setSectionResizeMode(1)
        self.header_list_tablewidget.setSelectionMode(QAbstractItemView.MultiSelection)

    def set_footer_list_tablewidget(self):

        self.footer_list_tablewidget.setColumnCount(1)
        self.footer_list_tablewidget.setHorizontalHeaderLabels(["맺음말"])

        try:
            self.footer_list_tablewidget.setRowCount(
                len(self.saved_data_footer[self.footer_topic_combobox.currentText()])
            )
            for i, footer in enumerate(self.saved_data_footer[self.footer_topic_combobox.currentText()]):
                self.footer_list_tablewidget.setItem(i, 0, QTableWidgetItem(footer))
        except Exception as e:
            pass

        self.footer_list_tablewidget.horizontalHeader().setSectionResizeMode(1)
        self.footer_list_tablewidget.setSelectionMode(QAbstractItemView.MultiSelection)

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

        # 머리글 관리
        header_groupbox = QGroupBox("머리글 관리")
        self.header_input_label = QLabel("머리글 관리")
        self.header_topic_combobox = QComboBox()
        self.header_input = QLineEdit()
        self.header_save_button = QPushButton("저장")
        self.header_remove_button = QPushButton("제거")
        self.header_list_tablewidget = QTableWidget()

        self.header_save_button.clicked.connect(self.header_save_button_clicked)
        self.header_remove_button.clicked.connect(self.header_remove_button_clicked)

        header_inner_layout = QGridLayout()
        header_inner_layout.addWidget(self.header_input_label, 0, 0, 1, 1)
        header_inner_layout.addWidget(self.header_topic_combobox, 0, 1, 1, 1)
        header_inner_layout.addWidget(self.header_input, 0, 2, 1, 1)
        header_inner_layout.addWidget(self.header_save_button, 0, 3, 1, 1)
        header_inner_layout.addWidget(self.header_remove_button, 0, 4, 1, 1)
        header_inner_layout.addWidget(self.header_list_tablewidget, 1, 2, 3, 1)
        header_groupbox.setLayout(header_inner_layout)

        self.header_topic_combobox.currentTextChanged.connect(self.set_header_list_tablewidget)

        # 맺음말 관리
        footer_groupbox = QGroupBox("맺음말 관리")
        self.footer_input_label = QLabel("맺음말 관리")
        self.footer_topic_combobox = QComboBox()
        self.footer_input = QLineEdit()
        self.footer_save_button = QPushButton("저장")
        self.footer_remove_button = QPushButton("제거")
        self.footer_list_tablewidget = QTableWidget()

        self.footer_save_button.clicked.connect(self.footer_save_button_clicked)
        self.footer_remove_button.clicked.connect(self.footer_remove_button_clicked)

        footer_inner_layout = QGridLayout()
        footer_inner_layout.addWidget(self.footer_input_label, 0, 0, 1, 1)
        footer_inner_layout.addWidget(self.footer_topic_combobox, 0, 1, 1, 1)
        footer_inner_layout.addWidget(self.footer_input, 0, 2, 1, 1)
        footer_inner_layout.addWidget(self.footer_save_button, 0, 3, 1, 1)
        footer_inner_layout.addWidget(self.footer_remove_button, 0, 4, 1, 1)
        footer_inner_layout.addWidget(self.footer_list_tablewidget, 1, 2, 3, 1)
        footer_groupbox.setLayout(footer_inner_layout)

        self.footer_topic_combobox.currentTextChanged.connect(self.set_footer_list_tablewidget)

        self.set_combobox()

        # 레이아웃 배치
        top_layout = QHBoxLayout()
        top_layout.addStretch(1)
        top_layout.addWidget(topic_groupbox, 7)
        top_layout.addStretch(1)

        mid_layout = QHBoxLayout()
        mid_layout.addStretch(1)
        mid_layout.addWidget(header_groupbox, 7)
        mid_layout.addStretch(1)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(footer_groupbox, 7)
        bottom_layout.addStretch(1)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addLayout(mid_layout)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)
