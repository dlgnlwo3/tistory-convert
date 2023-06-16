

if 1 == 1:
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from enum import Enum


class Words(Enum):
    # RANDOM_PATTERN = r"\$랜덤\$(.*?)\$랜덤/\$"
    RANDOM_START_WORD = "$랜덤$"
    RANDOM_END_WORD = "$/랜덤$"
    REPLACE_KEYWORD = '$키워드$'
    SENTENCE_SPLIT = '\n\n'









