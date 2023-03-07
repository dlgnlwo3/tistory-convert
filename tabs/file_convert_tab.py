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


class FileConvertTab(QWidget):

    # 초기화
    def __init__(self):

        super().__init__()
        self.initUI()

    def convert_sentence_button_clicked(self):

        # 값이 입력되어있는지 확인
        if self.input_sentence_textedit.toPlainText() == "":
            QMessageBox.information(self, "변환하기", f"입력된 값이 없습니다.")
            return

        # 치환 키워드
        convert_keyword = self.convert_keyword_input.text()
        if self.header_select_checkbox.isChecked() or self.footer_select_checkbox.isChecked():
            if self.convert_keyword_input.text() == "":
                print("치환 키워드 필수 입력")
                QMessageBox.information(self, "작업 시작", f"치환 키워드를 입력해주세요.")
                return
            print(f"convert_keyword: {convert_keyword}")

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

        # 양방향 작업
        ban_synonym = self.ban_synonym_input.text()
        if ban_synonym == "":
            ban_synonym_list = []
        else:
            ban_synonym_list = ban_synonym.split(",")
        original_sentence = self.input_sentence_textedit.toPlainText()
        sentence = original_sentence
        for i, row in df_two_way[:].iterrows():
            try:
                data = str(row["data"])

                if any(s in data for s in ban_synonym_list):
                    continue

                synonym_list = data.split(",")
                sentence = convert_sentence(sentence, synonym_list)

            except Exception as e:
                print(e)
                QMessageBox.information(self, "오류", f"작업 중 오류가 발생했습니다. \n{e}")
                return

        # 문단 랜덤 섞기 체크 시
        if self.shuffle_paragraphs_checkbox.isChecked():
            sentence_to_list = sentence.split(f"\n\n")
            print(sentence_to_list)

            random.shuffle(sentence_to_list)
            print(sentence_to_list)

            if len(sentence_to_list) > 0:
                sentence = f"\n\n".join(sentence_to_list)

        # 머리글 삽입
        if self.header_select_checkbox.isChecked():
            header_topic = self.header_topic_combobox.currentText()

            self.saved_data_header = get_save_data_HEADER()
            header: str = random.choice(self.saved_data_header[header_topic])

            header = header.replace("$키워드$", convert_keyword)
            header += f"\n\n"

            sentence = header + sentence

        # 맺음말 삽입
        if self.footer_select_checkbox.isChecked():
            footer_topic = self.footer_topic_combobox.currentText()

            self.saved_data_footer = get_save_data_FOOTER()
            footer: str = random.choice(self.saved_data_footer[footer_topic])

            footer = footer.replace("$키워드$", convert_keyword)
            footer = f"\n\n" + footer

            sentence = sentence + footer

        print()
        print(sentence)
        self.result_sentence_textedit.clear()
        self.result_sentence_textedit.setText(sentence)

    def retry_sentence_button_clicked(self):
        print("retry_sentence_button_clicked")

    def copy_sentence_button_clicked(self):
        print("copy_sentence_button_clicked")
        sentence = self.result_sentence_textedit.toPlainText()
        clipboard.copy(str(sentence))
        QMessageBox.information(self, "복사", f"클립보드에 복사되었습니다.")

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

    # 메인 UI
    def initUI(self):

        # 변환 금지어 입력
        ban_synonym_groupbox = QGroupBox()
        self.ban_synonym_input_label = QLabel("변환 금지어 입력")
        self.ban_synonym_input = QLineEdit("화려하게")

        ban_synonym_inner_layout = QHBoxLayout()
        ban_synonym_inner_layout.addWidget(self.ban_synonym_input_label)
        ban_synonym_inner_layout.addWidget(self.ban_synonym_input)
        ban_synonym_groupbox.setLayout(ban_synonym_inner_layout)

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

        # 치환 키워드 입력
        convert_keyword_groupbox = QGroupBox("치환 키워드 입력")
        self.convert_keyword_input = QLineEdit()

        convert_keyword_inner_layout = QHBoxLayout()
        convert_keyword_inner_layout.addWidget(self.convert_keyword_input)
        convert_keyword_groupbox.setLayout(convert_keyword_inner_layout)

        # 변환할 문장
        input_sentence_groupbox = QGroupBox("문장 입력")
        self.input_sentence_textedit = QTextEdit()
        self.input_sentence_textedit.setPlainText(
            f"폐어망·폐생수통이 '갤럭시 S23'으로 화려하게 변신\n\n'전자팔찌 끊고 도주' 김봉현 도운 친구 등 3명 기소\n\n결국 소비자들에게 돌아가는 혜택이 축소되는 결과로 이어질 수 있다고 예상했다."
        )
        self.convert_sentence_button = QPushButton("변환하기")

        self.convert_sentence_button.clicked.connect(self.convert_sentence_button_clicked)

        input_sentence_inner_layout = QGridLayout()
        input_sentence_inner_layout.addWidget(self.input_sentence_textedit, 0, 1, 1, 2)
        input_sentence_inner_layout.addWidget(self.convert_sentence_button, 1, 2, 1, 1)
        input_sentence_groupbox.setLayout(input_sentence_inner_layout)

        # 변환된 문장
        result_sentence_groupbox = QGroupBox("변환 결과")
        self.result_sentence_textedit = QTextEdit()
        self.retry_sentence_button = QPushButton("다시 변환")
        self.copy_sentence_button = QPushButton("복사하기")

        self.retry_sentence_button.clicked.connect(self.retry_sentence_button_clicked)
        self.copy_sentence_button.clicked.connect(self.copy_sentence_button_clicked)

        result_sentence_inner_layout = QGridLayout()
        result_sentence_inner_layout.addWidget(self.result_sentence_textedit, 0, 0, 1, 2)
        # result_sentence_inner_layout.addWidget(self.retry_sentence_button, 1, 0, 1, 1)
        result_sentence_inner_layout.addWidget(self.copy_sentence_button, 1, 1, 1, 1)
        result_sentence_groupbox.setLayout(result_sentence_inner_layout)

        # 레이아웃 배치
        top_layout = QHBoxLayout()
        top_layout.addStretch(1)
        top_layout.addWidget(ban_synonym_groupbox, 7)
        top_layout.addStretch(1)

        mid_layout = QHBoxLayout()
        mid_layout.addStretch(1)
        mid_layout.addWidget(shuffle_paragraphs_groupbox, 7)
        mid_layout.addStretch(1)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(header_select_groupbox, 3)
        bottom_layout.addWidget(footer_select_groupbox, 3)
        bottom_layout.addWidget(convert_keyword_groupbox, 1)
        bottom_layout.addStretch(1)

        sentence_layout = QHBoxLayout()
        sentence_layout.addStretch(1)
        sentence_layout.addWidget(input_sentence_groupbox, 4)
        sentence_layout.addWidget(result_sentence_groupbox, 4)
        sentence_layout.addStretch(1)

        layout = QVBoxLayout()
        layout.addLayout(top_layout, 1)
        layout.addLayout(mid_layout, 1)
        layout.addLayout(bottom_layout, 1)
        layout.addLayout(sentence_layout, 8)

        self.setLayout(layout)
