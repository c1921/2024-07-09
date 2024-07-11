from PyQt6.QtGui import QKeySequence
from PyQt6.QtCore import Qt

class Shortcuts:
    PAUSE_CONTINUE = QKeySequence(Qt.Key.Key_Space)
    SPEED_1X = QKeySequence(Qt.Key.Key_F1)
    SPEED_2X = QKeySequence(Qt.Key.Key_F2)
    SPEED_5X = QKeySequence(Qt.Key.Key_F3)
    SPEED_10X = QKeySequence(Qt.Key.Key_F4)
    SWITCH_TAB = QKeySequence(Qt.Key.Key_Tab)
