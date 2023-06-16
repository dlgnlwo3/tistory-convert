if 1 == 1:
    import sys
    import warnings
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    warnings.simplefilter("ignore", UserWarning)
    sys.coinit_flags = 2

from tkinter import *

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from common.chrome import *
from dtos.gui_dto import *
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from config import *

from tabs.search_tab import SearchTab
from tabs.setting_tab import SettingTab
from tabs.topic_tab import TopicTab
from tabs.synonym_convert_tab import SynonymConvertTab
from tabs.file_convert_tab import FileConvertTab
from tabs.synonym_multiple_convert_tab import SynonymMultipleConvertTab
from widgets.license_add_widget import LicenseAddWidget


# pyinstaller -n "tistory convert v2.0.1" -w --onefile --clean  "main.py" --icon "assets\icon.png" --noupx --add-data "venv\Lib\site-packages\newspaper;newspaper"


# def my_exception_hook(exctype, value, traceback):
#     print(exctype, value, traceback)
#     global_log_append(str(value))
#     sys._excepthook(exctype, value, traceback)

# sys.excepthook = my_exception_hook


class MainUI():
    # 초기화
    def __init__(self):
        self.licenseAddWidget = LicenseAddWidget()
        self.app_widget = AppWidget()
        self.licenseAddWidget.register_checked.connect(self.app_widget.initUI)
        result = self.licenseAddWidget.license_check()

        if result["is_valid"] == True:
            self.app_widget.initUI()
        else:
            self.licenseAddWidget.initUI()
            self.licenseAddWidget.show_warning_msg(result["error"])


class AppWidget(QWidget):
    def __init__(self):
        super().__init__()

    def initIcon(self):
        # 이미지 주소
        ICON_IMAGE_URL = "https://i.imgur.com/yUWPOGp.png"
        self.icon = QNetworkAccessManager()
        self.icon.finished.connect(self.set_window_icon_from_response)
        self.icon.get(QNetworkRequest(QUrl(ICON_IMAGE_URL)))

    # 가운데 정렬
    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

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

    def set_window_icon_from_response(self, http_response):
        pixmap = QPixmap()
        pixmap.loadFromData(http_response.readAll())
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)

    # 메인 UI
    def initUI(self):
        # 이미지 주소
        ICON_IMAGE_URL = "https://i.imgur.com/yUWPOGp.png"
        self.icon = QNetworkAccessManager()
        self.icon.finished.connect(self.set_window_icon_from_response)
        self.icon.get(QNetworkRequest(QUrl(ICON_IMAGE_URL)))

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
    main_ui = MainUI()
    sys.exit(app.exec())