if 1 == 1:
    import sys
    import warnings
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    warnings.simplefilter("ignore", UserWarning)
    sys.coinit_flags = 2
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from dtos.gui_dto import *
from datetime import timedelta
from timeit import default_timer as timer

from process.daum_search_process import DaumSearch
from common.utils import beepsound


# import debugpy


class DaumSearchThread(QThread):
    log_msg = Signal(str)
    search_finished = Signal()

    # 호출 시점
    def __init__(self):
        super().__init__()

    # guiDto세팅
    def setGuiDto(self, guiDto: GUIDto):
        self.guiDto = guiDto

    def run(self):
        try:
            # debugpy.debug_this_thread()

            self.log_msg.emit(f"작업 시작")
            start_time = timer()
            search = DaumSearch()
            search.setGuiDto(self.guiDto)
            search.setLogger(self.log_msg)
            search.work_start()
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

        self.search_finished.emit()

    def stop(self):
        try:
            self.terminate()
        except Exception as e:
            print(e)
