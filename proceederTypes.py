from enum import Enum

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

class Coordinates():
    def __init__(self):
        self.x = -1
        self.y = -1

    def set(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({},{})".format(self.x, self.y)

class Settings():
    def __init__(self):
        self.count = 0
        self.delay_s = 0
        self.proceederKey = ProceederKey.NONE

        self.startCoords = Coordinates()
        self.endCoords = Coordinates()

        self.folder = ""

    def __str__(self):
        settingsStrList = [
            "count: {}".format(self.count),
            "delay (s): {}".format(self.delay_s),
            "proceederKey: {}".format(self.proceederKey.name),
            "Coords: {} to {}".format(self.startCoords, self.endCoords),
            "folder: {}".format(self.folder) 
        ]

        return '\n'.join(settingsStrList)