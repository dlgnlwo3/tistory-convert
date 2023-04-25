# tkinter를 사용하기 위한 import
from main import MainUI
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from config import get_save_data_ACCOUNT, write_save_data_ACCOUNT
from features.google_sheet import login


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        saved_account = get_save_data_ACCOUNT()
        self.save_login_id = saved_account["id"]
        self.save_login_pw = saved_account["pw"]
        self.initUi()

    def set_window_icon_from_response(self, http_response):
        pixmap = QPixmap()
        pixmap.loadFromData(http_response.readAll())
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)

    def initUi(self):
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
        login_layout.addWidget(self.save_button, 1)
        login_groupbox.setLayout(login_layout)

        layout = QVBoxLayout()
        layout.addLayout(login_layout)
        self.setLayout(layout)

        # 앱 기본 설정
        self.setWindowTitle("Re.writer")
        self.resize(500, 600)
        self.show()

    def login_button_clicked(self):
        user_id = self.login_id_edit.text()
        user_pw = self.login_pw_edit.text()
        if login(user_id, user_pw):
            ex = MainUI()
        else:
            QMessageBox.warning(self, "아이디, 비밀번호를 확인해주세요.")
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
        mbox = QMessageBox()
        mbox.setText("저장하였습니다.")
        mbox.exec_()


def login():
    app = QApplication(sys.argv)
    ex = LoginForm()
    sys.exit(app.exec_())


if __name__ == "__main__":
    login()
