if 1 == 1:
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from enum import Enum


class ConvertHtml(Enum):
    COLOR_RED = 'color:#ff0000;'



