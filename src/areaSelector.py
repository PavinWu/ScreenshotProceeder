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
        self.screenShooter = ScreenShooter()

        self.screenshotLabel = QtWidgets.QLabel(self)
        self.layout = QtWidgets.QStackedLayout(self)
        self.layout.addWidget(self.screenshotLabel)

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

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
        self.__hidePixmapFullscreen__()

    def getCoords(self):
        pixmap = self.screenShooter.getWholeScreen()
        self.screenshotLabel = self.__showPixmapFullScreen__(pixmap)
        return self.beginCoords, self.endCoords

    def __showPixmapFullScreen__(self, pixmap):
        # TODO remove
        print("Label size: {} x {}", self.screenshotLabel.width(), self.screenshotLabel.height())
        screen = QtGui.QGuiApplication.primaryScreen()
        # TODO remove. incorrect screen size?
        print("Screen size: {} x {}", screen.geometry().width(), screen.geometry().height())

        self.screenshotLabel.setPixmap(pixmap.scaled(
                self.screenshotLabel.size(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation))
        self.show()

    def __hidePixmapFullscreen__(self):
        self.hide()

