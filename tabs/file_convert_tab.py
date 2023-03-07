import sys
import warnings

warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import *

from common.utils import *
from config import *
from features.convert_sentence import convert_sentence
from common.synonym_file import SynonymFile
import pandas as pd
import clipboard
import random


class FileConvertTab(QWidget):
    # 초기화
    def __init__(self):
        super().__init__()
        self.initUI()

    # 메인 UI
    def initUI(self):
        # 레이아웃 배치
        top_layout = QHBoxLayout()
        top_layout.addStretch(1)
        top_layout.addStretch(1)

        mid_layout = QHBoxLayout()
        mid_layout.addStretch(1)
        mid_layout.addStretch(1)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch(1)
        bottom_layout.addStretch(1)

        sentence_layout = QHBoxLayout()
        sentence_layout.addStretch(1)
        sentence_layout.addStretch(1)

        layout = QVBoxLayout()
        layout.addLayout(top_layout, 1)
        layout.addLayout(mid_layout, 1)
        layout.addLayout(bottom_layout, 1)
        layout.addLayout(sentence_layout, 1)

        self.setLayout(layout)
