from PySide6 import QtCore, QtWidgets
from areaSelector import AreaSelector
from screenShooter import ScreenShooter
from keyActuator import KeyActuator
from proceederTypes import *

from pathlib import Path
import time

QPoint = QtCore.QPoint

class SingletonShooterForQThread(QtCore.QRunnable):        
    def __init__(self):
        super().__init__()

    def setup(self, applicationSelectWait_s, settings, boundary, shooter, doneCallback):
        self.settings = settings
        self.boundary = boundary
        self.screenshooter = shooter
        self.doneCallback = doneCallback
        self.applicationSelectWait_s = applicationSelectWait_s

    def run(self):
        if (self.settings is not None) and (self.settings.isValid()) and (self.screenshooter is not None):
            self.screenshooter.getRepeatCroppedScreen(self.applicationSelectWait_s, self.settings)
        else:
            print("Settings invalid. Aborting ...")
        
        self.doneCallback()

class SetupView(QtWidgets.QWidget):

    applicationSelectWait_s = 5

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
        settings.startNum = self.screenshotStartNum.value()
        settings.delay_s = self.screenshotDelay_s.value()
        settings.proceederKey = self.proceederKeyComboBox.currentData()
        settings.folder = self.selectedFolderLabel.text()
        settings.beginCoords = self.boundary.begin
        settings.endCoords = self.boundary.end

        return settings

    def __defineWidgets__(self):
        self.screenshotCountLabel = "Number of screenshots: "
        self.screenshotCount = SetupView.__setupScreenshotCount__()
        self.screenshotStartNumLabel = "First screenshot file number: "
        self.screenshotStartNum = SetupView.__setupScreenshotStartNum__()
        self.screenshotDelayLabel = "Delay (s): "
        self.screenshotDelay_s = SetupView.__setupScreenshotDelay__()
        self.selectProceederLabel = "Proceeder Key: "
        self.proceederKeyComboBox = SetupView.__setupProceederKey__()

        self.selectAreaButton = QtWidgets.QPushButton("Select Area")
        self.selectedAreaLabel = QtWidgets.QLabel("[0, 0] to [0, 0]")

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
        self.topLayout.addRow(self.screenshotStartNumLabel, self.screenshotStartNum)
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
        self.setupWidgetList.append(self.screenshotStartNum)
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
                                       str(Path.home()),
                                       QtWidgets.QFileDialog.ShowDirsOnly
                                    |  QtWidgets.QFileDialog.DontResolveSymlinks)
        self.selectedFolderLabel.setText(str(self.selectedFolder))

    @QtCore.Slot()
    def __start__(self):
        self.__setWidgetEnableStateForCancel__()
        self.showMinimized()

        singletonShooter = SingletonShooterForQThread()
        singletonShooter.setup(SetupView.applicationSelectWait_s, self.getSettings(), self.boundary, self.screenShooter, self.__cancel__)
        QtCore.QThreadPool.globalInstance().start(singletonShooter)

    @QtCore.Slot()
    def __cancel__(self):
        self.__setWidgetEnableStateForSetup__()
        self.screenShooter.stopRepeatCroppedScreen()
        
        # Need to hide then show for the window to be restored ..
        self.hide()
        self.showNormal()

    @QtCore.Slot()
    def __selectArea__(self):
        self.hide()

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

    def __setupScreenshotCount__():
        defaultScreenshotCount = 1

        screenshotCount = QtWidgets.QSpinBox()
        screenshotCount.setValue(defaultScreenshotCount)
        screenshotCount.setMinimum(1)
        screenshotCount.setMaximum(9999)
        return screenshotCount

    def __setupScreenshotStartNum__():
        defaultStartNum = 0
        screenshotStartNum = QtWidgets.QSpinBox()
        screenshotStartNum.setValue(defaultStartNum)
        screenshotStartNum.setMinimum(0)
        screenshotStartNum.setMaximum(9998)
        return screenshotStartNum

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
        guideStrings.append("After pressing start, with in {} seconds, the user must ensure".format(SetupView.applicationSelectWait_s))
        guideStrings.append("the application they wish to proceed and take screenshot is in focus.")
        guideStrings.append("If you wish to stop the process before it completes, come back to")
        guideStrings.append("this window and press Cancel.")
        return guideStrings