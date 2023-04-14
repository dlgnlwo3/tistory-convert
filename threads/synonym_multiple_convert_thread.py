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
import time
from common.utils import beepsound

# import debugpy

from process.synonym_multiple_convert_process import SynonymMultipleConvert


class ConvertThread(QThread):
    log_msg = pyqtSignal(str)
    convert_finished = pyqtSignal()

    # 호출 시점
    def __init__(self):
        super().__init__()

    # guiDto세팅
    def setGuiDto(self, guiDto: GUIDto):
        self.guiDto = guiDto

    def run(self):
        try:
            # debugpy.debug_this_thread()

            self.log_msg.emit(f"유의어 변환 작업 시작")

            start_time = timer()

            # 작업 시작
            converter = SynonymMultipleConvert()

            converter.setGuiDto(self.guiDto)

            converter.setLogger(self.log_msg)

            converter.work_start()

            end_time = timer()

            progress_time = timedelta(seconds=end_time - start_time).seconds

            self.log_msg.emit(f"총 {str(progress_time)}초 소요되었습니다.")

        except Exception as e:
            print(f"작업 중 오류가 발생했습니다. {str(e)}")
            self.log_msg.emit(f"작업 중 오류가 발생했습니다. {str(e)}")

        if self.guiDto.system_sound_checkbox:
            print("알림음")
            beepsound()
            # playsound(
            #     r"D:\Consolework\tistory-convert-new\assets\thread_finished_sound.mp3"
            # )

        self.convert_finished.emit()

    def stop(self):
        try:
            self.terminate()
        except Exception as e:
            print(e)
