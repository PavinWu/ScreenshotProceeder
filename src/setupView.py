from PySide6 import QtCore, QtWidgets
from areaSelector import AreaSelector
from screenShooter import ScreenShooter
from proceederTypes import *
import time

QPoint = QtCore.QPoint

class SetupView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # instance variables
        self.setupWidgetList = []
        self.cancelWidgetList = []
        self.screenShooter = ScreenShooter()
        self.areaSelector = AreaSelector(self.screenShooter)
        self.boundary = Boundary()

        # setup
        self.__defineWidgets__()
        self.__setupConnections__()
        self.__setupLayouts__()

    def getSettings(self):
        settings = Settings()
        settings.count = self.screenshotCount.value()
        settings.delay_s = self.screenshotDelay_s.value()
        settings.proceederKey = self.proceederKeyComboBox.currentData()
        settings.beginCoords = QPoint()
        settings.endCoords = QPoint()
        settings.folder = self.selectedFolderLabel.text()
        
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
                                       "/home", # TODO Probably wont work on Windows
                                       QtWidgets.QFileDialog.ShowDirsOnly
                                    |  QtWidgets.QFileDialog.DontResolveSymlinks)
        self.selectedFolderLabel.setText(str(self.selectedFolder))

    @QtCore.Slot()
    def __start__(self):
        self.__setWidgetEnableStateForCancel__()

        # TODO perform start action

    @QtCore.Slot()
    def __cancel__(self):
        self.__setWidgetEnableStateForSetup__()

        # TODO perform cancel action

    @QtCore.Slot()
    def __selectArea__(self):
        self.__hideMainWindow__()   # TODO somehow hiding only activates when the method exits
        time.sleep(2)
        # self.areaSelector.selectCoords(self.__getSelectArea__)

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
        guideStrings.append("After starting, press TODO to stop taking screenshot")
        return guideStrings

# get view

# /int box - number of screenshots
# /delay between screenshot

# /path selector to select where to save file
# (not mvp) text box to specify filename
# /key to proceed the application
# /key to start selecting area
# /add button to start / cancel