if 1 == 1:
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import time
from dtos.gui_dto import GUIDto
from common.utils import global_log_append
from timeit import default_timer as timer
from datetime import timedelta, datetime
from dtos.top_blog_detail_dto import *
from config import *
import pandas as pd
import re
from docx import Document
from features.convert_sentence import (
    convert_from_db,
    shuffle_sentence,
    insert_header_to_sentence,
    insert_footer_to_sentence,
)
import random


class SynonymMultipleConvert:
    def __init__(self):
        self.run_time = str(datetime.now())[0:-10].replace(":", "")

    def setGuiDto(self, guiDto: GUIDto):
        self.guiDto = guiDto

    def setLogger(self, log_msg):
        self.log_msg = log_msg

    # 워드 저장
    def sentence_to_docx(self, file_name: str, sentence: str, limit=""):
        save_path = os.path.join(self.guiDto.convert_path, f"유의어 변환 {self.run_time}")

        if os.path.isdir(save_path) == False:
            os.mkdir(save_path)
        else:
            pass

        if limit == "":
            sentence_docx = os.path.join(save_path, f"{file_name}.docx")
        else:
            limit = str(limit)
            sentence_docx = os.path.join(save_path, f"{file_name}_{limit.zfill(2)}.docx")

        doc = Document()

        doc.add_paragraph(sentence)

        doc.save(sentence_docx)

        if limit == "":
            self.log_msg.emit(f"{file_name}.docx 저장 완료")
        else:
            limit = str(limit)
            self.log_msg.emit(f"{file_name}_{limit.zfill(2)}.docx 저장 완료")

    def get_sentence_from_file(self, file_path: str):
        sentence = ""

        # docx 파일인 경우
        if file_path.rfind(".docx") > -1:
            doc = Document(file_path)
            all_text = []
            for para in doc.paragraphs:
                all_text.append(para.text)
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        all_text.append(cell.text)
            all_text = " ".join(all_text)
            sentence = all_text

        # txt 파일인 경우
        elif file_path.rfind(".txt") > -1:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                sentence = text

        else:
            pass

        return sentence

    # 전체작업 시작
    def work_start(self):
        print(f"converter: work_start {self.run_time}")

        file: str
        for i, file in enumerate(self.guiDto.convert_list):
            file_path = os.path.join(self.guiDto.convert_path, file)
            file_format = file[file.rfind(".") :]

            # 파일 유효성 검사
            if os.path.isfile(file_path):
                print(file_path)
            else:
                continue

            # 파일에서 문자열 획득
            original_sentence = self.get_sentence_from_file(file_path)

            # 횟수 제한 기능
            for limit in range(1, self.guiDto.synonym_convert_limit + 1):
                print(limit)

                # 문자열 변환
                sentence, used_synonym_list = convert_from_db(
                    original_sentence, "", self.guiDto.df_two_way, self.guiDto.df_one_way
                )

                # 문단 랜덤 섞기 체크 시
                if self.guiDto.shuffle_paragraphs_check:
                    sentence = shuffle_sentence(sentence)

                # 머리글 삽입
                if self.guiDto.header_check:
                    header_topic = self.guiDto.header_topic
                    saved_data_header = get_save_data_HEADER()
                    header: str = random.choice(saved_data_header[header_topic])
                    sentence = insert_header_to_sentence(sentence, header, convert_keyword=file.rstrip(file_format))

                # 맺음말 삽입
                if self.guiDto.footer_check:
                    footer_topic = self.guiDto.footer_topic
                    saved_data_footer = get_save_data_FOOTER()
                    footer: str = random.choice(saved_data_footer[footer_topic])
                    sentence = insert_footer_to_sentence(sentence, footer, convert_keyword=file.rstrip(file_format))

                # print(sentence)

                # 문자열 파일 저장
                self.sentence_to_docx(file.rstrip(file_format), sentence, limit)


if __name__ == "__main__":
    converter = SynonymMultipleConvert()
    converter.work_start()
