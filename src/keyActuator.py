
### Seems to have a lot of problems doing this on Wayland
# import keyboard   # unmaintained!
# import pyautogui  # doesn't even import https://github.com/asweigart/pyautogui/issues/111 
# import pynput   # on Silverblue, seem to need to install python3-evdev: https://github.com/streamdeck-linux-gui/streamdeck-linux-gui/discussions/189
#   Still doesn't work after setup on Silverblue. Previously, on normal Fedora:
#   pynput seems to detect only after you have pressed a modifier key! (ctrl/alt/shift/key.cmd (win))
#   https://pynput.readthedocs.io/en/latest/limitations.html
#   Only XWayland application ? Works on Firefox
#   Seems key is detected, but need to input modifier key after. Input the key, then modifier key (e.g. shift)

from evdev import UInput, ecodes as e   
# need python3-evdev
# need: sudo usermod -a -G input $USER to get details about devices

from proceederTypes import ProceederKey

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
        evKeyId = self.keyToEvdevId(proceederKey)
        if evKeyId is not None:
            ui = UInput()
            ui.write(e.EV_KEY, evKeyId, 1)  # Press
            ui.write(e.EV_KEY, evKeyId, 0)  # Release
            ui.syn()
            ui.close()