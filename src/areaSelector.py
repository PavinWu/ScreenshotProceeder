from PySide6 import QtCore, QtWidgets, QtGui
import threading
from screenShooter import *

QRect = QtCore.QRect

class AreaSelector(QtWidgets.QWidget):
    def __init__(self, screenShooter):
        super().__init__()

        # Note that begin coords may be less or greater than end.
        self.beginCoords = QRect()
        self.endCoords = QRect()
        self.areaSelectedSem = threading.Semaphore()
        self.screenShooter = ScreenShooter()

        # Don't pass parent to have rubber band be top level.
        self.rubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)

    def mousePressEvent(self, event):
        self.beginCoords = event.pos()
        # TODO normalize coords here?
        self.rubberBand.setGeometry(QRect(self.beginCoords, QtCore.QSize()))
        self.rubberBand.show()

    def mouseMoveEvent(self, event):
        self.rubberBand.setGeometry(QRect(self.beginCoords, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        self.endCoords = event.pos()
        self.rubberBand.hide()
        # self.areaSelectedSem.release()

    def getCoords(self):
        pixmap = self.screenShooter.getWholeScreen()
        pixmap.save("pixmap.jpg")
        screenshotLabel = self.__showPixmapFullScreen__(pixmap)

        # self.setEnabled(True)

        # Looks like we need to create an overlay first.

        # self.areaSelectedSem.acquire()       
        # self.setEnabled(False)

        # TODO With this, ended up not showing anything??
        # self.__hidePixmapFullscreen__(screenshotLabel)

        return self.beginCoords, self.endCoords

    def __showPixmapFullScreen__(self, pixmap):

        screenshotLabel = QtWidgets.QLabel(self)
        # TODO uncomment
        screenshotLabel.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        screenshotLabel.setAlignment(QtCore.Qt.AlignCenter)
        screenshotLabel.setPixmap(pixmap.scaled(
                screenshotLabel.size(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation))
        screenshotLabel.showFullScreen()

        return screenshotLabel

    def __hidePixmapFullscreen__(self, screenshotLabel):
        screenshotLabel.setWindowFlags(self.windowFlags() & ~QtCore.Qt.FramelessWindowHint & ~QtCore.Qt.WindowStaysOnTopHint)
        screenshotLabel.hide()

