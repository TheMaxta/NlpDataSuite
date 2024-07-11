from enum import Enum

class ChopMethod(Enum):
    EXACT = 1
    SENTENCE = 2
    LINE_BREAK = 3
    WORD = 4