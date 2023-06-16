import sys
import warnings

warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from datetime import *

from common.utils import *
from config import *
from features.convert_sentence import (
    convert_from_db,
    shuffle_sentence,
    insert_header_to_sentence,
    insert_footer_to_sentence,
)

from common.synonym_file import SynonymFile
import pandas as pd
import clipboard
import random
from widgets.qline_edit_widget import CustomLineEdit

from enums.html_tag import ConvertHtml

class SynonymConvertTab(QWidget):
    # 초기화
    def __init__(self):
        super().__init__()
        self.initUI()

    def dict_sentence_to_red_sentence(self, dict_sentence: dict, used_idx_list: list):
        for sentence_i in dict_sentence.keys():
            to_sentence = dict_sentence[sentence_i]
            to_sentence = str(to_sentence)

            if to_sentence.find("<") > -1:
                to_sentence = "&lt;"
            elif to_sentence.find(">") > -1:
                to_sentence = "&gt;"

            if sentence_i in used_idx_list:
                to_sentence = f'<span style="{ConvertHtml.COLOR_RED.value}">{to_sentence}</span>'
            dict_sentence.update({sentence_i: to_sentence})
        return "".join(dict_sentence.values())
    

    def remove_edits_button_clicked(self):
        print('remove_edits_button_clicked')
        self.result_sentence_textedit.clear()
        self.input_sentence_textedit.clear()

        self.input_word_count_label.setText(" 0자  /")
        self.word_count_input_sentence_label.setText("0자")
        self.convert_result_count_label.setText("0자")


    def convert_sentence_button_clicked(self):
        # 값이 입력되어있는지 확인
        if self.input_sentence_textedit.toPlainText() == "":
            QMessageBox.information(self, "변환하기", f"입력된 값이 없습니다.")
            return

        # 치환 키워드
        convert_keyword = self.convert_keyword_input.text()
        if (
            self.header_select_checkbox.isChecked()
            or self.footer_select_checkbox.isChecked()
        ):
            if self.convert_keyword_input.text() == "":
                print("치환 키워드 필수 입력")
                QMessageBox.information(self, "작업 시작", f"치환 키워드를 입력해주세요.")
                return

        # 엑셀 DB 확인
        self.saved_data_synonym = get_save_data_SYNONYM()
        if self.saved_data_synonym[SaveFileSYNONYM.SYNONYM_FILE_SAVE_PATH.value] == "":
            print(f"엑셀DB 파일을 설정해주세요.")
            # self.log_append(f"저장 경로를 먼저 설정해주세요.")
            QMessageBox.information(self, "작업 시작", f"엑셀DB 파일을 설정해주세요.")
            return
        else:
            search_file_save_path = self.saved_data_synonym[
                SaveFileSYNONYM.SYNONYM_FILE_SAVE_PATH.value
            ]

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

        # 변환 금지어
        ban_synonym = self.ban_synonym_input.text()

        # 원본 텍스트
        sentence = self.input_sentence_textedit.toPlainText()

        # 변환 작업
        converted_word_count = 0
        try:
            dict_sentence, used_idx_list = convert_from_db(
                sentence, ban_synonym, df_two_way, df_one_way
            )
            sentence = self.dict_sentence_to_red_sentence(dict_sentence, used_idx_list)

        except Exception as e:
            if str(e).find("Cannot choose from an empty sequence") > -1:
                QMessageBox.warning(
                    self,
                    "오류 발생",
                    # f"[{str(e)[:str(e).find(':')]}] 유의어 데이터를 확인해주세요. \n{e}",
                     "'a=b=c'와 같은 형태로 DB를 수정해 주세요",
                )
                return

        # 문단 랜덤 섞기 체크 시
        if self.shuffle_paragraphs_checkbox.isChecked():
            sentence = shuffle_sentence(sentence)

        # 머리글 삽입
        if self.header_select_checkbox.isChecked():
            header_topic = self.header_topic_combobox.currentText()
            self.saved_data_header = get_save_data_HEADER()
            header: str = random.choice(self.saved_data_header[header_topic])
            header = f'<span style="color : blue">{header}</span>'
            sentence = insert_header_to_sentence(sentence, header, convert_keyword)

        # 맺음말 삽입
        if self.footer_select_checkbox.isChecked():
            footer_topic = self.footer_topic_combobox.currentText()
            self.saved_data_footer = get_save_data_FOOTER()
            footer: str = random.choice(self.saved_data_footer[footer_topic])
            footer = f'<span style="color : blue">{footer}</span>'
            sentence = insert_footer_to_sentence(sentence, footer, convert_keyword)

        sentence = sentence.replace(f"\n", "<br />")
        self.result_sentence_textedit.clear()
        self.result_sentence_textedit.setText(sentence)


        # 변환결과 표시 
        # html 제거된 원본 sentence의 크기
        # span stype red로 둘러싸인 html 태그 안의 갯수
        before_total_count,converted_word_count =  get_word_count_from_html(sentence, ConvertHtml.COLOR_RED.value)

        # 현재 글자수 체크
        self.input_word_count_label.setText(f" {format(before_total_count, ',')}자  /")
        self.convert_result_count_label.setText(f" {format(converted_word_count, ',')}자")


    def retry_sentence_button_clicked(self):
        print("retry_sentence_button_clicked")

    def copy_sentence_button_clicked(self):
        print("copy_sentence_button_clicked")
        sentence = self.result_sentence_textedit.toPlainText()

        LF = '\n'
        CRLF = '\r\n'
        CR = '\r'

        # sentence = sentence.replace(CRLF, LF).replace(CR, LF)
        sentence = sentence.replace(LF, CRLF)


        clipboard.copy(str(sentence))
        QMessageBox.information(self, "복사", f"클립보드에 복사되었습니다.")

    def header_select_checkbox_changed(self):
        if self.header_select_checkbox.isChecked():
            self.set_header_topic_combobox()
        else:
            self.header_topic_combobox.clear()

    def footer_select_checkbox_changed(self):
        if self.footer_select_checkbox.isChecked():
            self.set_footer_topic_combobox()
        else:
            self.footer_topic_combobox.clear()

    def set_header_topic_combobox(self):
        self.saved_data_topic = get_save_data_topic()
        self.header_topic_combobox.clear()

        for i, topic in enumerate(self.saved_data_topic[SaveFileTopic.TOPIC.value]):
            self.header_topic_combobox.addItem(f"{topic}")

    def set_footer_topic_combobox(self):
        self.saved_data_topic = get_save_data_topic()
        self.footer_topic_combobox.clear()

        for i, topic in enumerate(self.saved_data_topic[SaveFileTopic.TOPIC.value]):
            self.footer_topic_combobox.addItem(f"{topic}")

    def on_input_sentence_textedit_keyReleaseEvent(self, event):
        text = self.input_sentence_textedit.toPlainText()
        word_count = get_word_count_without_empty(text)
        self.word_count_input_sentence_label.setText(f" {format(word_count, ',')}자")


    def on_result_sentence_textedit_keyReleaseEvent(self, event):

        text = self.result_sentence_textedit.toHtml()
        before_total_count,converted_word_count =  get_word_count_from_html(text, ConvertHtml.COLOR_RED.value)

        # 현재 글자수 체크
        self.input_word_count_label.setText(f" {format(before_total_count, ',')}자 /")
        self.convert_result_count_label.setText(f" {format(converted_word_count, ',')}자")


    # 메인 UI
    def initUI(self):
        # 변환 금지어 입력
        ban_synonym_groupbox = QGroupBox()
        self.ban_synonym_input_label = QLabel("변환 금지어 입력")
        self.ban_synonym_input = CustomLineEdit()
        self.ban_synonym_input.setPlaceholderText('여러 금지어를 "="로 구분하여 입력할 수 있습니다. ex)바나나 효능=다이어트')

        self.remove_edits_button = QPushButton("전체지우기")
        self.remove_edits_button.clicked.connect(
            self.remove_edits_button_clicked
        )

        ban_synonym_inner_layout = QHBoxLayout()
        ban_synonym_inner_layout.addWidget(self.ban_synonym_input_label)
        ban_synonym_inner_layout.addWidget(self.ban_synonym_input)
        ban_synonym_inner_layout.addWidget(self.remove_edits_button)
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

        self.header_select_checkbox.stateChanged.connect(
            self.header_select_checkbox_changed
        )

        # 맺음말 삽입
        footer_select_groupbox = QGroupBox()
        self.footer_select_checkbox = QCheckBox("맺음말 삽입")
        self.footer_topic_combobox = QComboBox()

        footer_select_inner_layout = QHBoxLayout()
        footer_select_inner_layout.addWidget(self.footer_select_checkbox)
        footer_select_inner_layout.addWidget(self.footer_topic_combobox)
        footer_select_groupbox.setLayout(footer_select_inner_layout)

        self.footer_select_checkbox.stateChanged.connect(
            self.footer_select_checkbox_changed
        )

        # 치환 키워드 입력
        convert_keyword_groupbox = QGroupBox("치환 키워드 입력")
        self.convert_keyword_input = CustomLineEdit()

        convert_keyword_inner_layout = QHBoxLayout()
        convert_keyword_inner_layout.addWidget(self.convert_keyword_input)
        convert_keyword_groupbox.setLayout(convert_keyword_inner_layout)

        # 변환할 문장
        input_sentence_groupbox = QGroupBox("문장 입력")
        self.input_sentence_textedit = QPlainTextEdit()
        #         self.input_sentence_textedit.setPlainText(
        #             f"""그룹 BTS 정국이 3년 전 매입한 서울 이태원동 소재 2층짜리 단독 주택을 허물고 그 자리에 새 저택을 짓고 있다.
        # 5일 머니투데이에 따르면 정국은 지난해 7월 용산구청으로부터 이태원동에 있는 단독주택에 대한 신축 허가를 받았다. 정국은 지난 2020년 12월 이태원동에 위치한 주택을 76억3000만원에 매입했다.
        # 정국이 짓는 단독주택은 지하 2층-지상 3층 규모로 약 1160제곱미터(약 351평)에 달하는 대저택으로 알려졌다. 대지 면적은 633.05㎡(191평), 건축면적은 348.05㎡(105평)이다. 현재 기초 공사 중으로 완공 예정일은 오는 2024년 5월 31일이다.
        # 그가 짓고 있는 이태원동은 삼성그룹 오너, 최태원(SK그룹 회장), 이명희(신세계그룹 회장) 등이 살고 있는 곳으로 알려졌다."""
        #         )

        # self.input_sentence_textedit.setPlainText("바나나 효능이 좋습니다.")
        self.input_sentence_textedit.keyReleaseEvent = self.on_input_sentence_textedit_keyReleaseEvent


        self.word_count_input_sentence_label = QLabel("0자")

        self.convert_sentence_button = QPushButton("변환하기")
        self.convert_sentence_button.clicked.connect(
            self.convert_sentence_button_clicked
        )

        input_sentence_inner_layout = QGridLayout()
        input_sentence_inner_layout.addWidget(self.input_sentence_textedit, 0, 1, 1, 2)
        input_sentence_inner_layout.addWidget(self.word_count_input_sentence_label, 1, 1, 1, 1)
        input_sentence_inner_layout.addWidget(self.convert_sentence_button, 1, 2, 1, 1)
        input_sentence_groupbox.setLayout(input_sentence_inner_layout)

        # 변환된 문장
        result_sentence_groupbox = QGroupBox("변환 결과")
        self.result_sentence_textedit = QTextEdit()
        self.retry_sentence_button = QPushButton("다시 변환")
        self.copy_sentence_button = QPushButton("복사하기")

        self.input_word_count_label = QLabel(" 0자  /")
        self.slush_label = QLabel("/")
        self.convert_result_count_label = QLabel("0자")
        self.fixed_convert_label = QLabel("변환")
        self.convert_result_count_label.setStyleSheet(ConvertHtml.COLOR_RED.value)


        self.result_sentence_textedit.keyReleaseEvent = self.on_result_sentence_textedit_keyReleaseEvent
        self.retry_sentence_button.clicked.connect(self.retry_sentence_button_clicked)
        self.copy_sentence_button.clicked.connect(self.copy_sentence_button_clicked)

        result_sentence_inner_layout = QGridLayout()
        result_sentence_inner_layout.addWidget(
            self.result_sentence_textedit, 0, 0, 1, 17
        )
        result_sentence_inner_layout.addWidget(self.input_word_count_label, 1, 0, 1, 1)
        # result_sentence_inner_layout.addWidget(self.slush_label, 1, 2, 1, 1)
        result_sentence_inner_layout.addWidget(self.convert_result_count_label, 1, 1, 1, 1)
        result_sentence_inner_layout.addWidget(self.fixed_convert_label, 1, 2, 1, 1)
        result_sentence_inner_layout.addWidget(self.copy_sentence_button, 1, 10, 1, 7)
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
