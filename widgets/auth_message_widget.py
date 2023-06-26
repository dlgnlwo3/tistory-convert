from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
import time


def QuitMessage(second: int):
    message_box = QMessageBox()
    message_box.setWindowTitle("프로그램 중복실행발견")
    message_box.setText("프로그램이 10초뒤에 자동으로 종료됩니다.")
    message_box.exec()
    time.sleep(second)
    message_box.close()
