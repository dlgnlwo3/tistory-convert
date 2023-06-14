from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest

from features.google_sheet import login_sheet
from config import get_save_data_ACCOUNT, write_save_data_ACCOUNT

class LoginWidget(QWidget):

    login_checked = Signal()

    def __init__(self):
        super().__init__()
        saved_account = get_save_data_ACCOUNT()
        self.saved_login_id = saved_account["id"]
        self.saved_login_pw = saved_account["pw"]

    # 가운데 정렬
    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_window_icon_from_response(self, http_response):
        pixmap = QPixmap()
        pixmap.loadFromData(http_response.readAll())
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)

    def initIcon(self):
        # 이미지 주소
        ICON_IMAGE_URL = "https://i.imgur.com/yUWPOGp.png"
        self.icon = QNetworkAccessManager()
        self.icon.finished.connect(self.set_window_icon_from_response)
        self.icon.get(QNetworkRequest(QUrl(ICON_IMAGE_URL)))

    def login_button_clicked(self):
        user_id = self.login_id_edit.text()
        user_pw = self.login_pw_edit.text()

        if not user_id or not user_pw:
            QMessageBox.warning(self, "로그인실패", "아이디, 비밀번호를 확인해주세요.")
            return

        if login_sheet(user_id, user_pw):
            QMessageBox.information(self, "로그인성공", "로그인 하였습니다.")
            self.login_checked.emit()
            self.destroy()

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
        self.login_id_edit = QLineEdit(f"{self.saved_login_id}")
        self.login_id_edit.setPlaceholderText("아이디")
        self.login_id_edit.setFixedWidth = 500

        self.login_pw_edit = QLineEdit(f"{self.saved_login_pw}")
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
        self.setWindowTitle("Re.writer Login")
        self.resize(450, 150)
        self.center()
        self.show()
