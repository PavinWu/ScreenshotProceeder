from PySide6 import QtCore, QtWidgets, QtGui
import threading
from screenShooter import *
from proceederTypes import *

QRect = QtCore.QRect

class AreaSelector(QtWidgets.QWidget):
    def __init__(self, screenShooter):
        super().__init__()

        # Note that begin coords may be less or greater than end.
        self.beginCoords = QRect()
        self.endCoords = QRect()
        self.screenShooter = ScreenShooter()
        self.sideRatio = 1
        self.commBoundary = CommunicateBoundary()

        self.screenshotLabel = QtWidgets.QLabel(self)
        self.layout = QtWidgets.QStackedLayout(self)
        self.layout.addWidget(self.screenshotLabel)

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

    def mousePressEvent(self, event):
        self.beginCoords = event.pos()
        # TODO normalize coords here?
        print("Drawing begin coord at {}, {}", self.beginCoords.x, self.beginCoords.y)
        self.rubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)
        self.rubberBand.setGeometry(QRect(self.beginCoords, QtCore.QSize()))
        self.rubberBand.show()

    def mouseMoveEvent(self, event):
        self.rubberBand.setGeometry(QRect(self.beginCoords, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        self.endCoords = event.pos()
        self.rubberBand.hide()
        self.__hidePixmapFullscreen__()

        boundary = Boundary()
        boundary.begin = self.beginCoords
        boundary.end = self.endCoords
        # TODO HiDPI scaling
        self.commBoundary.signal.emit(boundary) # TODO test passing int for now
        # TODO This works if user doesn't come back to the main screen/
        # TODO disconnect

    def selectCoords(self, getCoordsCallback):
        # Can do this!: https://stackoverflow.com/questions/37252756/simplest-way-for-pyqt-threading
        # https://doc.qt.io/qtforpython-6/tutorials/basictutorial/signals_and_slots.html#signals-and-slots
        # Note: in all these cases, the signal is NOT the signal object. It's created inside a QObject, and use the name in there.
        pixmap = self.screenShooter.getTempWholeScreen()
        self.__showPixmapFullScreen__(pixmap)
        self.commBoundary.signal.connect(getCoordsCallback) # TODO no need to connect again if already connected?

    def __showPixmapFullScreen__(self, pixmap):
        screen = QtGui.QGuiApplication.primaryScreen()

        # Screen size may be different to actual pixel dimensions if using HiDPI screen.
        # See https://doc.qt.io/qt-6/highdpi.html
        print("Screen size: {} x {}", screen.geometry().width(), screen.geometry().height())
        print("Pixmap size: {} x {}", pixmap.width(), pixmap.height())
        print("Side ratio = {}", pixmap.width())

        # TODO pass 
        # TODO centre pixmap? (seems to be a bit off?)
        self.screenshotLabel.setPixmap(pixmap.scaled(
                screen.size(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation))
        self.show()

    def __hidePixmapFullscreen__(self):
        self.hide()

