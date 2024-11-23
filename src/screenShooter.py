from PySide6 import QtCore, QtWidgets, QtGui
import platform

class ScreenShooter(QtWidgets.QWidget):
    def __init__(self, keyActuator):
        super().__init__()
        self.keyActuator = keyActuator

    def getTempWholeScreen(self):
        return getWholeScreen("/tmp/screenshot_proceeder_screenbg.jpg")

    def getCroppedScreen(self, picPath, rect):
        pixmap = getWholeScreen(picPath)
        return pixmap.copy(rect)

    def getWholeScreen(self, picPath):
        # Note: The Qt's screen grabber doesn't work on Wayland. Assume Linux is using Wayland.
        # https://bugreports.qt.io/browse/QTBUG-34976?focusedCommentId=276038&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel
        # 
        # Use Spectacle instead.
        # TODO refactor so we reuse some parts for non-whole screen screen grabing

        if platform.system() == "Linux":
            print("Linux detected. Note: require Spectacle to work.")

            process = QtCore.QProcess()
            print("starting spectacle")
            process.start("spectacle", ["-b", "-m", "-n", "-o", picPath])
            if (process.waitForFinished()):
                print("execution finished")

                pixmap = QtGui.QPixmap()
                pixmap.load(picPath)
                return pixmap
            else:
                # TODO better error handling
                raise RuntimeError("The universal wayland screen capture adapter requires Grim as " +
                         "the screen capture component of wayland. If the screen " +
                         "capture component is missing, please install it!")
        
        # TODO non-Wayland Linux and other platforms
        # else:
        #     screen = QtGui.QGuiApplication.primaryScreen()
        #     window = self.windowHandle()  
        #     if window:
        #         screen = window.screen()
        #     if not screen:
        #         raise RuntimeError("Nope")  # TODO
        #     pixmap = screen.grabWindow(0)

        return pixmap

    def getRepeatCroppedScreen(self, picPath, rect, key, dur):
        pass                                                                                 

