
# Add requirements:
# - pillow
# - 

# License

# arguments: number of key presses, key press, application, wait time for each key

# capture screenshot
#   https://medium.com/@rahbarysina/1-practical-python-how-to-take-screenshot-using-python-605469329025
# show UI to user
#   
# read four corners from user
    # check that it makes up four corners
# create folder
# repeat
    # select appliation, capture screenshot (and crop) and send key
# (optional) combine into PDF?

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