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

    # TODO mouse event not registered for non-main window???
    # Apparently, these mouse events require main window by default ...
    def mousePressEvent(self, event):
        self.beginCoords = event.pos()
        # TODO normalize coords here?
        print("Drawing start coord at {}, {}", self.beginCoords.x, self.beginCoords.y)
        self.rubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)
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
        self.setEnabled(True)
        screenshotLabel = self.__showPixmapFullScreen__(pixmap)


        # Looks like we need to create an overlay first.

        # self.areaSelectedSem.acquire()       
        # self.setEnabled(False)
        # self.__hidePixmapFullscreen__(screenshotLabel)

        return self.beginCoords, self.endCoords

    def __showPixmapFullScreen__(self, pixmap):

        screenshotLabel = QtWidgets.QLabel(self)

        print("Label size: {} x {}", screenshotLabel.width(), screenshotLabel.height())
        screen = QtGui.QGuiApplication.primaryScreen()
        # TODO incorrect screen size when using external screen
        print("Screen size: {} x {}", screen.geometry().width(), screen.geometry().height())
        
        screenshotLabel.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        screenshotLabel.setAlignment(QtCore.Qt.AlignCenter)
        # TODO set qlabel size to screen size.
        # screenshotLabel.setPixmap(pixmap.scaled(
        #         screenshotLabel.size(),
        #         QtCore.Qt.KeepAspectRatio,
        #         QtCore.Qt.SmoothTransformation))
        screenshotLabel.setPixmap(pixmap)
        screenshotLabel.showFullScreen()

        return screenshotLabel

    def __hidePixmapFullscreen__(self, screenshotLabel):
        screenshotLabel.setWindowFlags(self.windowFlags() & ~QtCore.Qt.FramelessWindowHint & ~QtCore.Qt.WindowStaysOnTopHint)
        screenshotLabel.hide()

