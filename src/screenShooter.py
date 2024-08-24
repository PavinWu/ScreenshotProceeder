from PySide6 import QtCore, QtWidgets, QtGui

class ScreenShooter(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

    def getWholeScreen(self):
        screen = QtGui.QGuiApplication.primaryScreen()
        window = self.windowHandle()
        if window:
            screen = window.screen()
        if not screen:
            raise RuntimeError("Nope")  # TODO
        return screen.grabWindow(0)