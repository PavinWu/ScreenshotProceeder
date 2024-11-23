# import keyboard   # unmaintained!
import pynput

class KeyActuator:
    # pynput seems to detect only after you have pressed a modifier key! (ctrl/alt/shift/key.cmd (win))
    # https://pynput.readthedocs.io/en/latest/limitations.html
    # Only XWayland application ? Works on Firefox
    # Seems key is detected, but need to input modifier key after. Input the key, then modifier key (e.g. shift)
    def __init__(self):
        pass




