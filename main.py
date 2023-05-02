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
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from config import *

from tabs.search_tab import SearchTab
from tabs.setting_tab import SettingTab
from tabs.topic_tab import TopicTab
from tabs.synonym_convert_tab import SynonymConvertTab
from tabs.file_convert_tab import FileConvertTab
from tabs.synonym_multiple_convert_tab import SynonymMultipleConvertTab
from features.google_sheet import login_sheet
from config import get_save_data_ACCOUNT, write_save_data_ACCOUNT
from common.utils import global_log_append


# pyinstaller -n "tistory convert v1.1.8 파일일괄변환 수정" -w --onefile --clean  "main.py" --icon "assets\icon.png" --noupx --add-data "venv\Lib\site-packages\newspaper;newspaper"
def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    global_log_append(str(value))
    sys._excepthook(exctype, value, traceback)


sys.excepthook = my_exception_hook


class MainUI(QWidget):
    is_login = False

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
        saved_account = get_save_data_ACCOUNT()
        self.save_login_id = saved_account["id"]
        self.save_login_pw = saved_account["pw"]
        # UI
        super().__init__()
        self.initIcon()

        if self.is_login:
            self.initUI()  # 로그인 완료후 기본 MainUI 보여주기
        else:
            self.initLoginUI()  # 로그인 안되어있으면 로그인 시도

    def initIcon(self):
        # 이미지 주소
        ICON_IMAGE_URL = "https://i.imgur.com/yUWPOGp.png"
        self.icon = QNetworkAccessManager()
        self.icon.finished.connect(self.set_window_icon_from_response)
        self.icon.get(QNetworkRequest(QUrl(ICON_IMAGE_URL)))

    # 가운데 정렬
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # # 프로그램 닫기 클릭 시
    def closeEvent(self, event):
        quit_msg = "프로그램을 종료하시겠습니까?"
        reply = QMessageBox.question(
            self, "프로그램 종료", quit_msg, QMessageBox.Yes, QMessageBox.No
        )

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

    def login_button_clicked(self):
        user_id = self.login_id_edit.text()
        user_pw = self.login_pw_edit.text()

        if not user_id or not user_pw:
            QMessageBox.warning(self, "로그인실패", "아이디, 비밀번호를 확인해주세요.")
            return

        if login_sheet(user_id, user_pw):
            self.is_login = True
            QMessageBox.information(self, "로그인성공", "로그인 하였습니다.")
            self.destroy()
            self.__init__()
            return

        else:
            QMessageBox.warning(self, "로그인실패", "아이디, 비밀번호를 확인해주세요.")
            return

    # 저장 파일
    def save_button_clicked(self):
        login_id = self.login_id_edit.text()
        login_pw = self.login_pw_edit.text()

        question_msg = "저장하시겠습니까?"
        reply = QMessageBox.question(
            self, "계정 저장", question_msg, QMessageBox.Yes, QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        write_save_data_ACCOUNT({"id": login_id, "pw": login_pw})
        QMessageBox.information(self, "저장성공", "저장 하였습니다.")

    def initLoginUI(self):
        # 이미지 주소
        ICON_IMAGE_URL = "https://i.imgur.com/yUWPOGp.png"
        self.icon = QNetworkAccessManager()
        self.icon.finished.connect(self.set_window_icon_from_response)
        self.icon.get(QNetworkRequest(QUrl(ICON_IMAGE_URL)))

        # 계정
        login_groupbox = QGroupBox("로그인")
        self.login_id_edit = QLineEdit(f"{self.save_login_id}")
        self.login_id_edit.setPlaceholderText("아이디")
        self.login_id_edit.setFixedWidth = 500

        self.login_pw_edit = QLineEdit(f"{self.save_login_pw}")
        self.login_pw_edit.setEchoMode(QLineEdit.Password)
        self.login_pw_edit.setPlaceholderText("비밀번호")
        self.login_pw_edit.setFixedWidth = 500

        self.login_button = QPushButton("로그인")
        self.login_button.clicked.connect(self.login_button_clicked)

        self.save_button = QPushButton("저장")
        self.save_button.clicked.connect(self.save_button_clicked)

        login_layout = QHBoxLayout()
        login_layout.addWidget(self.login_id_edit, 2)
        login_layout.addWidget(self.login_pw_edit, 2)
        login_layout.addWidget(self.login_button, 1)
        login_layout.addWidget(self.save_button, 1)
        login_groupbox.setLayout(login_layout)

        layout = QVBoxLayout()
        layout.addWidget(login_groupbox)
        self.setLayout(layout)

        # 앱 기본 설정
        self.setWindowTitle("Re.writer")
        self.resize(450, 150)
        self.show()

    # 메인 UI
    def initUI(self):
        # 탭 초기화
        self.search_tab = SearchTab()
        self.setting_tab = SettingTab()
        self.topic_tab = TopicTab()
        self.synonym_convert_tab = SynonymConvertTab()
        self.synonym_multiple_convertTab = SynonymMultipleConvertTab()
        self.file_convert_tab = FileConvertTab()

        # 탭 추가
        tabs = QTabWidget()
        tabs.addTab(self.search_tab, "수집")
        tabs.addTab(self.synonym_convert_tab, "유의어 변환 에디터")
        tabs.addTab(self.synonym_multiple_convertTab, "유의어 일괄 변환")
        tabs.addTab(self.file_convert_tab, "파일 변환")
        tabs.addTab(self.setting_tab, "설정")
        tabs.addTab(self.topic_tab, "주제 설정")

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)
        self.setLayout(vbox)

        # 앱 기본 설정
        self.setWindowTitle("Re.writer")
        self.resize(1200, 800)
        self.center()
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainUI()
    sys.exit(app.exec_())
