from enum import Enum
from PySide6.QtCore import QPoint, Signal, QObject

class ProceederKey(Enum):
    NONE  = 0,
    SPACE = 1, 
    ENTER = 2,
    RIGHT = 3,
    LEFT  = 4,
    DOWN  = 5,
    UP    = 6

class Settings():
    def __init__(self):
        self.count = 0
        self.delay_s = 0
        self.proceederKey = ProceederKey.NONE

        self.beginCoords = QPoint()
        self.endCoords = QPoint()

        self.folder = ""

    def __str__(self):
        settingsStrList = [
            "count: {}".format(self.count),
            "delay (s): {}".format(self.delay_s),
            "proceederKey: {}".format(self.proceederKey.name),
            "Coords: ({}, {}) to ({}, {})".format(
                self.beginCoords.x(), 
                self.beginCoords.y(), 
                self.endCoords.x(),
                self.endCoords.y()),
            "folder: {}".format(self.folder) 
        ]

        return '\n'.join(settingsStrList)

class Boundary():
    begin = QPoint()
    end = QPoint()

class CommunicateBoundary(QObject):
    signal = Signal(Boundary)
