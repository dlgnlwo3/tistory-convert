from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from configs.tistory_convert_config import TistoryConverterConfig as Config
from configs.tistory_convert_config import TistoryConverterData as ConfigData
from common.utils import get_mac_address, global_log_append
from common.valid import is_email_valid
from api_config import API_URL
import requests
from http import HTTPStatus
import time
from widgets.qline_edit_widget import CustomLineEdit
import json
class LicenseAddWidget(QWidget):

    register_checked = Signal()

    def __init__(self):
        super().__init__()
        self.initConfig()

    def initConfig(self):
        self.config = Config()
        __saved_data = self.config.get_data()
        self.saved_data = self.config.dict_to_data(__saved_data)
        self.license_key = self.saved_data.license_key
        self.email = self.saved_data.email
        
    # # 프로그램 닫기 클릭 시
    def closeEvent(self, event):
        quit_msg = "프로그램을 종료하시겠습니까?"
        reply = QMessageBox.question(self, "프로그램 종료", quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            print(f"프로그램을 종료합니다.")
            event.accept()
        else:
            print(f"종료 취소")
            event.ignore()
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

    # 등록 파일
    def register_button_clicked(self):
        license_key = self.license_key_edit.text()
        email = self.email_edit.text()

        if not license_key and not email:
            QMessageBox.warning(self, "등록실패", f"제품키와 이메일을 입력해주세요")
            return
        elif not is_email_valid(email):
            QMessageBox.warning(self, "등록실패", f"올바르지 않은 이메일 양식입니다.")
            return

        question_msg = "등록하시겠습니까?"
        reply = QMessageBox.question(
            self, "라이센스 등록", question_msg, QMessageBox.Yes, QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return
        
        mac_address = get_mac_address()

        dict_save = {"license_key": license_key,"email": email}

        url = f"{API_URL}/register/"
        try:
            datas=  {
            "customer_email": email,
            "license_key": license_key,
            "mac_address": mac_address
            }
            # 맥주소 다르게 한 경우
            # datas.update({"mac_address" : "2dd22:2d:2:2:dd"})
            response = requests.post(url, json=datas, timeout=5)
            print(response)
            print(response.text)

            if HTTPStatus.CREATED == response.status_code:
                Config().write_data(dict_save)
                time.sleep(2)
                QMessageBox.information(self, "등록 성공", "등록 하였습니다. 프로그램을 종료하고 다시 시작해주세요.")
            elif HTTPStatus.INTERNAL_SERVER_ERROR == response.status_code:
                QMessageBox.warning(self, "등록 실패", "서버에 오류가 발생하였습니다. 관리자에게 문의해주세요.")
                global_log_append(response.text)
            else:
                global_log_append(response.text)
                js_data = json.loads(response.text)
                error = js_data["error"]
                QMessageBox.warning(self, "등록 실패", error)
                return

        except Exception as e:
            print(e)
            raise Exception(e)
        

    def license_check(self):
        # 컴퓨터 로컬 안에 license_key가 존재한다면 해당 license_key + mac_Address로 존재여부, 유효기간을 체크하여 존재체크한다.
        # 존재하면 리턴
        print(self.license_key)
        print(self.email)
        print('')

        check_result = dict(
            is_valid=False,
            error = ""
        )

        if self.license_key:

            mac_address = get_mac_address()

            url = f"{API_URL}/license/"
            try:
                datas=  {
                "license_key": self.license_key,
                "mac_address": mac_address
                }
                # 맥주소 다르게 한 경우
                # datas.update({"mac_address" : "2dd22:2d:2:2:dd"})
                response = requests.post(url, json=datas, timeout=5)
                global_log_append(response.text)

                if HTTPStatus.OK == response.status_code:
                    time.sleep(2)
                    check_result.update({"is_valid":True})
                elif HTTPStatus.INTERNAL_SERVER_ERROR == response.status_code:
                    check_result.update({"error": "서버에 오류가 발생하였습니다. 관리자에게 문의해주세요."})
                else:
                    data = response.json()
                    error = data["error"]
                    check_result.update({"error":error})

            except Exception as e:
                print(e)
                raise Exception(e)
        else:
            check_result = dict(
                is_valid=False,
                error = "등록된 제품키가 없습니다."
            )
        return check_result
    

    def show_warning_msg(self, msg):
        QMessageBox.warning(self, "제품키 확인", msg)


    def initUI(self):

        # 이미지 주소
        ICON_IMAGE_URL = "https://i.imgur.com/yUWPOGp.png"
        self.icon = QNetworkAccessManager()
        self.icon.finished.connect(self.set_window_icon_from_response)
        self.icon.get(QNetworkRequest(QUrl(ICON_IMAGE_URL)))

        # 계정
        register_groupbox = QGroupBox("등록정보")

        license_key_label = QLabel("제품키")
        self.license_key_edit = CustomLineEdit(f"{self.license_key}")
        self.license_key_edit.setPlaceholderText("제품키")
        self.license_key_edit.setFixedWidth = 500


        email_label = QLabel("이메일")
        self.email_edit = CustomLineEdit(f"{self.email}")
        self.email_edit.setPlaceholderText("이메일주소")
        self.email_edit.setFixedWidth = 500

        self.register_button = QPushButton("제품등록")
        self.register_button.clicked.connect(self.register_button_clicked)
        self.register_button.setFixedHeight(40)

        register_layout = QGridLayout()
        register_layout.addWidget(license_key_label, 0, 0, 1, 1)
        register_layout.addWidget(self.license_key_edit, 0, 1, 1, 4)
        register_layout.addWidget(email_label, 1, 0, 1, 1)
        register_layout.addWidget(self.email_edit, 1, 1, 1, 4)
        register_layout.addWidget(self.register_button, 2, 0, 1, 5)
        register_groupbox.setLayout(register_layout)

        layout = QVBoxLayout()
        layout.addWidget(register_groupbox)
        self.setLayout(layout)

        # 앱 기본 설정
        self.setWindowTitle("Re.writer 제품키 등록")
        self.resize(600, 250)
        self.center()
        self.show()

