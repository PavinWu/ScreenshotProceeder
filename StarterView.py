from PySide6 import QtCore, QtWidgets

class StarterView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Setup GUI widgets for configuring the taking of screenshots
        self.screenshotCount = StarterView.__setupScreenshotCount__()
        self.screenshotDelay_s = StarterView.__setupScreenshotDelay__()

        self.selectAreaButton = QtWidgets.QPushButton("Select Area")
        self.selectedAreaLabel = QtWidgets.QLabel("[0,0] to [1920, 1080]")   # TODO get full screen resolution

        self.selectFolderButton = QtWidgets.QPushButton("Select Screenshot Folder")
        self.selectedFolderLabel = QtWidgets.QLabel("")  # TODO wrap to fit

        guideStrings = StarterView.__getGuideStrings__()
        self.guideLabels = [QtWidgets.QLabel(st) for st in guideStrings]
        self.startButton = QtWidgets.QPushButton("Start")
        self.cancelButton = QtWidgets.QPushButton("Cancel")

        # Setup connections
        self.selectFolderButton.clicked.connect(self.__selectScreenshotFolder__)

        # Setup layouts
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.topLayout = QtWidgets.QFormLayout()
        self.bottomLayout = QtWidgets.QGridLayout()
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)

        self.topLayout.addRow("Number of screenshots: ", self.screenshotCount)
        self.topLayout.addRow("Delay (s): ", self.screenshotDelay_s)
        
        self.bottomLayout.addWidget(self.selectFolderButton, 0, 0)
        self.bottomLayout.addWidget(self.selectedFolderLabel, 0, 1)
        self.bottomLayout.addWidget(self.selectAreaButton, 1, 0)
        self.bottomLayout.addWidget(self.selectedAreaLabel, 1, 1)
        for id, label in enumerate(self.guideLabels):
            # TODO Centre alignment
            self.bottomLayout.addWidget(label, id+2, 0, 1, -1)
        self.bottomLayout.addWidget(self.startButton, len(self.guideLabels)+3, 0)
        self.bottomLayout.addWidget(self.cancelButton, len(self.guideLabels)+3, 1)

    @QtCore.Slot()
    def __selectScreenshotFolder__(self):
        self.selectedFolder = QtWidgets.QFileDialog.getExistingDirectory(self, 
                                       "Open Directory",
                                       "/home",
                                       QtWidgets.QFileDialog.ShowDirsOnly
                                    |  QtWidgets.QFileDialog.DontResolveSymlinks)
        self.selectedFolderLabel.setText(str(self.selectedFolder))

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
# text box to specify filename
# key to proceed the application
# /key to start selecting area
# /add button to start / cancel