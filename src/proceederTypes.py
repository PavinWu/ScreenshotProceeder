from enum import Enum
from PySide6.QtCore import QPoint

class ProceederKey(Enum):
    # TODO use actual key id required by the library.
    NONE  = 0,
    SPACE = 1, 
    ENTER = 2,
    RIGHT = 3,
    LEFT  = 4,
    DOWN  = 5,
    UP    = 6,
    TAB   = 7,
    PAGE_DOWN = 8,
    PAGE_UP   = 9,
    HOME  = 10,
    END   = 11

class Settings():
    def __init__(self):
        self.count = 0
        self.delay_s = 0
        self.proceederKey = ProceederKey.NONE

        self.startCoords = QPoint()
        self.endCoords = QPoint()

        self.folder = ""

    def __str__(self):
        settingsStrList = [
            "count: {}".format(self.count),
            "delay (s): {}".format(self.delay_s),
            "proceederKey: {}".format(self.proceederKey.name),
            "Coords: ({}, {}) to ({}, {})".format(
                self.startCoords.x(), 
                self.startCoords.y(), 
                self.endCoords.x(),
                self.endCoords.y()),
            "folder: {}".format(self.folder) 
        ]

        return '\n'.join(settingsStrList)