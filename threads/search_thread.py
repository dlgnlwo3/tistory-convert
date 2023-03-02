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
from dtos.gui_dto import *
from datetime import timedelta
from timeit import default_timer as timer
from process.instagram_follow_process import InstagramFollow


import debugpy


class SearchThread(QThread):

    log_msg = pyqtSignal(str)
    search_finished = pyqtSignal()

    # 호출 시점
    def __init__(self):
        super().__init__()

    # guiDto세팅
    def setGuiDto(self, guiDto: GUIDto):
        self.guiDto = guiDto

    def run(self):
        try:
            debugpy.debug_this_thread()

            self.log_msg.emit(f"작업 시작")

            start_time = timer()

            instagramFollow = InstagramFollow()

            instagramFollow.setGuiDto(self.guiDto)

            instagramFollow.setLogger(self.log_msg)

            instagramFollow.work_start()

            end_time = timer()

            progress_time = timedelta(seconds=end_time - start_time).seconds

            self.log_msg.emit(f"총 {str(progress_time)}초 소요되었습니다.")

        except Exception as e:
            print(f"작업 중 오류가 발생했습니다. {str(e)}")
            self.log_msg.emit(f"작업 중 오류가 발생했습니다. {str(e)}")

        self.search_finished.emit()

    def stop(self):
        try:
            self.terminate()
        except Exception as e:
            print(e)
