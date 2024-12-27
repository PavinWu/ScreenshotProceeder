from PySide6 import QtWidgets
import sys

from setupView import SetupView
from areaSelector import *
from screenShooter import *

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    setupView = SetupView()
    setupView.show()

    sys.exit(app.exec())