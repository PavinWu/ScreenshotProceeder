# inspired by code from https://github.com/asweigart/pyautogui/issues/111

from evdev import UInput, ecodes as e

from proceederTypes import ProceederKey
import platform

class KeyActuator:
    def __init__(self):
        pass

    def keyToEvdevId(self, proceederKey):
        match proceederKey:
            case ProceederKey.ENTER:
                return e.KEY_ENTER
            case ProceederKey.SPACE:
                return e.KEY_SPACE
            case ProceederKey.RIGHT:
                return e.KEY_RIGHT
            case ProceederKey.LEFT:
                return e.KEY_LEFT
            case ProceederKey.DOWN:
                return e.KEY_DOWN
            case ProceederKey.UP:
                return e.KEY_UP
            case _:
                return None

    def proceed(self, proceederKey):
        if platform.system() == "Linux":
            evKeyId = self.keyToEvdevId(proceederKey)
            if evKeyId is not None:
                ui = UInput()
                ui.write(e.EV_KEY, evKeyId, 1)  # Press
                ui.write(e.EV_KEY, evKeyId, 0)  # Release
                ui.syn()
                ui.close()
        else:
            raise NotImplementedError("Only support Linux (Fedora Gnome)")