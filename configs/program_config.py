import os
from enum import Enum
from datetime import datetime
import json
from mimetypes import MimeTypes


class ProgramConfig:
    def __init__(self):
        self.company_name = "consolework"
        self.program_id = "tistory_converter"
        self.output_folder_name = "output"
        self.encoding = "utf-8"
        self.app_data_path = os.path.join(os.getenv("APPDATA"), self.company_name)
        self.program_path = os.path.join(self.app_data_path, self.program_id)
        self.exe_path = os.getcwd()  # 프로그램이 실행되는 exe파일 경로
        self.log_folder_name = "log"
        self.log_folder_path = os.path.join(self.program_path, self.log_folder_name)
        self.image_folder_name = "image"
        self.init_folder()

    def init_folder(self):
        # app_data_path
        if os.path.isdir(self.app_data_path) == False:
            os.mkdir(self.app_data_path)

        # program_path
        if os.path.isdir(self.program_path) == False:
            os.mkdir(self.program_path)

        # log_path
        if not os.path.isdir(self.log_folder_path):
            os.mkdir(self.log_folder_path)

    def create_output_folder(self):
        pass

        # # output폴더
        # if not os.path.isdir(self.output_folder_name):
        #     os.mkdir(self.output_folder_name)

        # # 오늘자 ouptut폴더
        # self.today_output_folder = os.path.join(
        #     os.getcwd(), self.output_folder_name, datetime.today().strftime("%Y%m%d")
        # )
        # if not os.path.isdir(self.today_output_folder):
        #     os.mkdir(self.today_output_folder)

        # self.image_folder_path = os.path.join(self.today_output_folder, self.image_folder_name)
        # if not os.path.isdir(self.image_folder_path):
        #     os.mkdir(self.image_folder_path)
