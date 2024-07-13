from PySide6 import QtCore, QtWidgets

class StarterView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()



        guideLabel = "When starting a count down of TODO seconds will appear." + \
            "\nSelect the application you want to proceed before the countdown ends" + \
            "\nAfter starting, press TODO to stop taking screenshot"
        self.guideLabel = QtWidgets.QLabel(guideLabel)
        self.startButton = QtWidgets.QPushButton("Start")
        self.cancelButton = QtWidgets.QPushButton("Cancel")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.guideLabel)
        self.layout.addWidget(self.startButton)
        self.layout.addWidget(self.cancelButton)

    


# get view

# int box - number of screenshots
# delay between screenshot
# path selector to select where to save file
# text box to specify filename
# key to proceed the application
# key to start selecting area

# add button to start / cancel