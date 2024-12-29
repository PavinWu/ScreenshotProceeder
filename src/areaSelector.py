from PySide6 import QtCore, QtWidgets, QtGui
import threading
from screenShooter import *
from proceederTypes import *

QRect = QtCore.QRect

class AreaSelector(QtWidgets.QWidget):
    def __init__(self, screenShooter):
        super().__init__()

        self.beginCoords = None
        self.endCoords = None
        self.screenShooter = screenShooter
        self.hdpiScaling = 1
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

        # Make begin coords top left, and end coords bottom right
        if boundary.begin.x() > boundary.end.x():
            boundary.begin = QPoint(self.endCoords.x(), boundary.begin.y())
            boundary.end = QPoint(self.beginCoords.x(), boundary.end.y())
            print(boundary.begin, boundary.end)

        if boundary.begin.y() > boundary.end.y():
            boundary.begin = QPoint(boundary.begin.x(), self.endCoords.y())
            boundary.end = QPoint(boundary.end.x(), self.beginCoords.y())
            print(boundary.begin, boundary.end)
        
        boundary.begin *= self.hdpiScaling
        boundary.end *= self.hdpiScaling
        
        self.commBoundary.signal.emit(boundary)

        # Disconnect. See https://doc.qt.io/qt-6/signalsandslots.html
        # TODO try catch somehow?
        self.commBoundary.signal.disconnect()

    def selectCoords(self, getCoordsCallback):
        # Can do this!: https://stackoverflow.com/questions/37252756/simplest-way-for-pyqt-threading
        # https://doc.qt.io/qtforpython-6/tutorials/basictutorial/signals_and_slots.html#signals-and-slots
        # Note: in all these cases, the signal is NOT the signal object. It's created inside a QObject, and use the name in there.
        pixmap = self.screenShooter.getTempWholeScreen()
        self.__showPixmapFullScreen__(pixmap)
        self.commBoundary.signal.connect(getCoordsCallback)

    def __showPixmapFullScreen__(self, pixmap):
        screen = QtGui.QGuiApplication.primaryScreen()

        # Screen size may be different to actual pixel dimensions if using HiDPI screen.
        # See https://doc.qt.io/qt-6/highdpi.html
        print("Screen size: {} x {}", screen.geometry().width(), screen.geometry().height())
        print("Pixmap size: {} x {}", pixmap.width(), pixmap.height())

        # Assuming pixmap gives the real screen resolution, and screen gives the 'appearance' resolution. 
        self.hdpiScaling = pixmap.width() / screen.geometry().width()

        self.screenshotLabel.setPixmap(pixmap.scaled(
                screen.size(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation))
        self.showFullScreen()

    def __hidePixmapFullscreen__(self):
        self.hide()

