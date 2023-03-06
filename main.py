if 1 == 1:
    import sys
    import warnings
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    warnings.simplefilter("ignore", UserWarning)
    sys.coinit_flags = 2

from tkinter import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import datetime
from common.chrome import *
from dtos.gui_dto import *
from common.utils import global_log_append
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from config import *

from tabs.search_tab import SearchUI
from tabs.setting_tab import SettingUI
from tabs.topic_tab import TopicUI

# 오류 발생 시 프로그램 강제종료 방지
def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    global_log_append(str(value))
    sys._excepthook(exctype, value, traceback)


sys.excepthook = my_exception_hook

# pyinstaller -n "tistory sample v0.0.2" -w --onefile --clean "main.py" --icon "assets\tistory.ico" --additional-hooks-dir=.


class MainUI(QWidget):

    # 초기화
    def __init__(self):

        print(f"LOG_FOLDER_NAME: {LOG_FOLDER_NAME}")
        print(f"PROGRAM_PATH: {PROGRAM_PATH}")
        print(f"USER_SAVE_PATH_DAUM: {USER_SAVE_PATH_DAUM}")
        print(f"USER_SAVE_PATH_GOOGLE: {USER_SAVE_PATH_GOOGLE}")
        print(f"USER_SAVE_PATH_SETTING: {USER_SAVE_PATH_SETTING}")
        print(f"USER_SAVE_PATH_SYNONYM: {USER_SAVE_PATH_SYNONYM}")
        print(f"USER_SAVE_PATH_TOPIC: {USER_SAVE_PATH_TOPIC}")
        print(f"USER_SAVE_PATH_HEADER: {USER_SAVE_PATH_HEADER}")
        print(f"USER_SAVE_PATH_FOOTER: {USER_SAVE_PATH_FOOTER}")

        # UI
        super().__init__()
        self.initUI()

    # 가운데 정렬
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 프로그램 닫기 클릭 시
    def closeEvent(self, event):
        quit_msg = "프로그램을 종료하시겠습니까?"
        reply = QMessageBox.question(self, "프로그램 종료", quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            print(f"프로그램을 종료합니다.")
            event.accept()
        else:
            print(f"종료 취소")
            event.ignore()

    def set_window_icon_from_response(self, http_response):
        pixmap = QPixmap()
        pixmap.loadFromData(http_response.readAll())
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)

    # 메인 UI
    def initUI(self):

        # 이미지 주소
        ICON_IMAGE_URL = "https://i.imgur.com/S8uiUDk.png"
        self.icon = QNetworkAccessManager()
        self.icon.finished.connect(self.set_window_icon_from_response)
        self.icon.get(QNetworkRequest(QUrl(ICON_IMAGE_URL)))

        # 탭 초기화
        self.search_tab = SearchUI()
        self.setting_tab = SettingUI()
        self.topic_tab = TopicUI()

        # 탭 추가
        tabs = QTabWidget()
        tabs.addTab(self.search_tab, "수집")
        tabs.addTab(self.setting_tab, "설정")
        tabs.addTab(self.topic_tab, "주제 설정")

        vbox = QVBoxLayout()

        vbox.addWidget(tabs)
        self.setLayout(vbox)

        # 앱 기본 설정
        self.setWindowTitle("tistory")
        self.resize(1200, 800)
        self.center()
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainUI()
    sys.exit(app.exec_())
