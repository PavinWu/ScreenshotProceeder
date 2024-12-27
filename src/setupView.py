from PySide6 import QtCore, QtWidgets
from areaSelector import AreaSelector
from screenShooter import ScreenShooter
from keyActuator import KeyActuator
from proceederTypes import *
import time

QPoint = QtCore.QPoint

class SingletonShooterForQThread(QtCore.QRunnable):        
    def __init__(self):
        super().__init__()

    def setup(self, settings, boundary, shooter, doneCallback):
        self.settings = settings
        self.boundary = boundary
        self.screenshooter = shooter
        self.doneCallback = doneCallback

    def run(self):
        if (self.settings is not None) and (self.screenshooter is not None):
            self.screenshooter.getRepeatCroppedScreen(
                self.settings.folder, 
                self.settings.delay_s, 
                QtCore.QRect(self.boundary.begin, self.boundary.end),
                self.settings.proceederKey, 
                self.settings.count
            )
            self.doneCallback()

class SetupView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # instance variables
        self.setupWidgetList = []
        self.cancelWidgetList = []
        self.keyActuator = KeyActuator()
        self.screenShooter = ScreenShooter(self.keyActuator)
        self.areaSelector = AreaSelector(self.screenShooter)
        self.boundary = Boundary()

        # setup
        self.__defineWidgets__()
        self.__setupConnections__()
        self.__setupLayouts__()

        # TODO restrict size

    def getSettings(self):
        settings = Settings()
        settings.count = self.screenshotCount.value()
        settings.delay_s = self.screenshotDelay_s.value()
        settings.proceederKey = self.proceederKeyComboBox.currentData()
        settings.folder = self.selectedFolderLabel.text()

        return settings
        
        # TODO validation

    def __defineWidgets__(self):
        self.screenshotCountLabel = "Number of screenshots: "
        self.screenshotCount = SetupView.__setupScreenshotCount__()
        self.screenshotDelayLabel = "Delay (s): "
        self.screenshotDelay_s = SetupView.__setupScreenshotDelay__()
        self.selectProceederLabel = "Proceeder Key: "
        self.proceederKeyComboBox = SetupView.__setupProceederKey__()

        self.selectAreaButton = QtWidgets.QPushButton("Select Area")
        self.selectedAreaLabel = QtWidgets.QLabel("[0,0] to [1920, 1080]")   # TODO get full screen resolution

        self.selectFolderButton = QtWidgets.QPushButton("Select Screenshot Folder")
        self.selectedFolderLabel = QtWidgets.QLabel("")  # TODO wrap to fit

        guideStrings = SetupView.__getGuideStrings__()
        self.guideLabels = [QtWidgets.QLabel(st) for st in guideStrings]
        self.startButton = QtWidgets.QPushButton("Start")
        self.cancelButton = QtWidgets.QPushButton("Cancel")

    def __setupConnections__(self):
        self.selectFolderButton.clicked.connect(self.__selectScreenshotFolder__)
        self.selectAreaButton.clicked.connect(self.__selectArea__)
        self.startButton.clicked.connect(self.__start__)
        self.cancelButton.clicked.connect(self.__cancel__)

    def __setupLayouts__(self):
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.topLayout = QtWidgets.QFormLayout()
        self.bottomLayout = QtWidgets.QGridLayout()
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)

        self.topLayout.addRow(self.screenshotCountLabel, self.screenshotCount)
        self.topLayout.addRow(self.screenshotDelayLabel, self.screenshotDelay_s)
        self.topLayout.addRow(self.selectProceederLabel, self.proceederKeyComboBox)
        
        self.bottomLayout.addWidget(self.selectFolderButton, 0, 0)
        self.bottomLayout.addWidget(self.selectedFolderLabel, 0, 1)
        self.bottomLayout.addWidget(self.selectAreaButton, 1, 0)
        self.bottomLayout.addWidget(self.selectedAreaLabel, 1, 1)
        for id, label in enumerate(self.guideLabels):
            # TODO Centre alignment
            self.bottomLayout.addWidget(label, id+2, 0, 1, -1)
        self.bottomLayout.addWidget(self.startButton, len(self.guideLabels)+3, 0)
        self.bottomLayout.addWidget(self.cancelButton, len(self.guideLabels)+3, 1)

        # Set widget states
        self.cancelButton.setEnabled(False)  # disable until in progress
        self.setupWidgetList.append(self.screenshotCount)
        self.setupWidgetList.append(self.screenshotDelay_s)
        self.setupWidgetList.append(self.proceederKeyComboBox)
        self.setupWidgetList.append(self.selectAreaButton)
        self.setupWidgetList.append(self.selectFolderButton)
        self.setupWidgetList.append(self.startButton)
        self.cancelWidgetList.append(self.cancelButton)

    @QtCore.Slot()
    def __selectScreenshotFolder__(self):
        self.selectedFolder = QtWidgets.QFileDialog.getExistingDirectory(self, 
                                       "Open Directory",
                                       "/home/vinwu/Documents/test", # TODO Probably wont work on Windows. TODO update
                                       QtWidgets.QFileDialog.ShowDirsOnly
                                    |  QtWidgets.QFileDialog.DontResolveSymlinks)
        self.selectedFolderLabel.setText(str(self.selectedFolder))

    @QtCore.Slot()
    def __start__(self):
        self.__setWidgetEnableStateForCancel__()
        # QtCore.QMetaObject.invokeMethod(self, "__startAction__", QtCore.Qt.QueuedConnection)

        # TODO minimise main window (NOT hide! - want user to be able to cancel)
        # TODO not allow start until all OK (including box)
        singletonShooter = SingletonShooterForQThread()
        singletonShooter.setup(self.getSettings(), self.boundary, self.screenShooter, self.__cancel__)
        QtCore.QThreadPool.globalInstance().start(singletonShooter)

        # TODO done event

    @QtCore.Slot()
    def __cancel__(self):
        self.__setWidgetEnableStateForSetup__()
        # TODO maximise
        self.screenShooter.stopRepeatCroppedScreen()

    @QtCore.Slot()
    def __selectArea__(self):
        self.__hideMainWindow__()

        # Defer execution until the Qt thread gets to update things in its update queue (after return of function).
        # Otherwise the function called will be executed first, and GUI won't be updated at the right time.
        ## obj, name of slot, connection type
        QtCore.QMetaObject.invokeMethod(self, "__callSelectCoords__", QtCore.Qt.QueuedConnection)

        # No error, but not hide
        # QtCore.QMetaObject.invokeMethod(self, "__callSelectCoords__", QtCore.Qt.AutoConnection)
        
        # Not work
        ## QtCore.QMetaObject.invokeMethod(self, areaSelector.selectCoords, self.__getSelectArea__)
        ## QtCore.QMetaObject.invokeMethod(self.areaSelector, selectCoords, self.__getSelectArea__)

    @QtCore.Slot()
    def __callSelectCoords__(self):
        time.sleep(0.5)     # Allow time for animation to complete
        self.areaSelector.selectCoords(self.__getSelectArea__)

    # @QtCore.Slot()
    # def __startAction__(self):
    #     self.screenShooter.getRepeatCroppedScreen()

    @QtCore.Slot(Boundary)
    def __getSelectArea__(self, boundary):
        self.boundary = boundary
        self.selectedAreaLabel.setText("[{}, {}] to [{}, {}]".format(
            boundary.begin.x(), boundary.begin.y(), boundary.end.x(), boundary.end.y()))
        self.__setWidgetEnableStateForSetup__()

    def __setWidgetEnableStateForSetup__(self):
        for widget in self.setupWidgetList:
            widget.setEnabled(True)
        for widget in self.cancelWidgetList:
            widget.setEnabled(False)
        self.show()

    def __setWidgetEnableStateForCancel__(self):
        for widget in self.setupWidgetList:
            widget.setEnabled(False)
        for widget in self.cancelWidgetList:
            widget.setEnabled(True)

    def __hideMainWindow__(self):
        # Tried:
        # - self.hide()
        # TODO somehow hiding only activates when the method exits .... turns out you have to move mouse before it hides ... what???
        # - resize to 0: no change.
        # - show minimized
        # - hide then sleep then show doesn't fix it...
        # What if you start a nwe thread? (so that hide window is the last thing?)
        # https://forum.qt.io/topic/145801/treeview-only-updates-when-mouse-is-moved-over-it/2  ?
        # Actually you could type something, not have to be mouse.
        # https://stackoverflow.com/questions/25544652/qt-widget-element-doesnt-want-to-hide
        self.hide()

    def __setupScreenshotCount__():
        defaultScreenshotCount = 1

        screenshotCount = QtWidgets.QSpinBox()
        screenshotCount.setValue(defaultScreenshotCount)
        screenshotCount.setMinimum(1)
        return screenshotCount

    def __setupScreenshotDelay__():
        defaultScreenshotDelay_s = 5

        screenshotDelay_s = QtWidgets.QSpinBox()
        screenshotDelay_s.setValue(defaultScreenshotDelay_s)
        screenshotDelay_s.setMinimum(0)
        screenshotDelay_s.setMaximum(3600)
        return screenshotDelay_s

    def __setupProceederKey__():
        proceederKeyComboBox = QtWidgets.QComboBox()
        for k in ProceederKey:
            proceederKeyComboBox.addItem(k.name, k)
        return proceederKeyComboBox

    def __getGuideStrings__():
        guideStrings = []
        guideStrings.append("")
        guideStrings.append("When starting a count down of TODO seconds will appear.")
        guideStrings.append("Select the application you want to proceed before the countdown ends")
        guideStrings.append("If you want to stop the process before it completes, press Cancel on this window")
        return guideStrings

# get view

# /int box - number of screenshots
# /delay between screenshot

# /path selector to select where to save file
# (not mvp) text box to specify filename
# /key to proceed the application
# /key to start selecting area
# /add button to start / cancel