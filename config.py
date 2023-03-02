import os
from enum import Enum
from datetime import datetime
import json
from mimetypes import MimeTypes

COMPANY_NAME = "consolework"
PROGRAM_ID = "tistory-convert"
APP_DATA_PATH = os.path.join(os.getenv("APPDATA"), COMPANY_NAME)

PROGRAM_PATH = os.path.join(APP_DATA_PATH, PROGRAM_ID)

if os.path.isdir(APP_DATA_PATH) == False:
    os.mkdir(APP_DATA_PATH)

if os.path.isdir(PROGRAM_PATH) == False:
    os.mkdir(PROGRAM_PATH)


USER_SAVE_PATH_DAUM = os.path.join(PROGRAM_PATH, f"{PROGRAM_ID}_DAUM.txt")


def get_save_data_daum():
    saved_data = None
    if os.path.isfile(USER_SAVE_PATH_DAUM):
        with open(USER_SAVE_PATH_DAUM, "r", encoding="utf-8") as f:
            saved_data = json.loads(f.read())
    return saved_data


def write_save_data_daum(dict_save: dict):

    if os.path.isfile(USER_SAVE_PATH_DAUM):
        os.remove(USER_SAVE_PATH_DAUM)
        with open(USER_SAVE_PATH_DAUM, "w", encoding="utf-8") as f:
            f.write(json.dumps((dict_save)))
            f.close()
    else:
        with open(USER_SAVE_PATH_DAUM, "w", encoding="utf-8") as f:
            f.write(json.dumps((dict_save)))
            f.close()

    return dict_save


class SaveFileDaum(Enum):
    DAUM = "daum"


# 저장데이터 없는 경우 초기화
if not get_save_data_daum():
    write_save_data_daum({SaveFileDaum.DAUM.value: []})



USER_SAVE_PATH_GOOGLE = os.path.join(PROGRAM_PATH, f"{PROGRAM_ID}_GOOGLE.txt")


def get_save_data_google():
    saved_data = None
    if os.path.isfile(USER_SAVE_PATH_GOOGLE):
        with open(USER_SAVE_PATH_GOOGLE, "r", encoding="utf-8") as f:
            saved_data = json.loads(f.read())
    return saved_data


def write_save_data_google(dict_save: dict):

    if os.path.isfile(USER_SAVE_PATH_GOOGLE):
        os.remove(USER_SAVE_PATH_GOOGLE)
        with open(USER_SAVE_PATH_GOOGLE, "w", encoding="utf-8") as f:
            f.write(json.dumps((dict_save)))
            f.close()
    else:
        with open(USER_SAVE_PATH_GOOGLE, "w", encoding="utf-8") as f:
            f.write(json.dumps((dict_save)))
            f.close()

    return dict_save


class SaveFileGoogle(Enum):
    GOOGLE = "google"


# 저장데이터 없는 경우 초기화
if not get_save_data_google():
    write_save_data_google({SaveFileGoogle.GOOGLE.value: []})


# ------------- 로그파일 경로 생성 시작 ------------- #

LOG_FOLDER_NAME = "log"
LOG_FOLDER_PATH = os.path.join(PROGRAM_PATH, LOG_FOLDER_NAME)
if not os.path.isdir(LOG_FOLDER_PATH):
    os.mkdir(LOG_FOLDER_PATH)
