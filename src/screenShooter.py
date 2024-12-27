from PySide6 import QtCore, QtWidgets, QtGui
import platform
import os
import subprocess

class ScreenShooter(QtWidgets.QWidget):
    def __init__(self, keyActuator):
        super().__init__()
        self.keyActuator = keyActuator
        self.stopRepeatScreenshot = False

    def getWholeScreen(self, picPath, timeDelay=0):
        # Note: The Qt's screen grabber doesn't work on Wayland. Assume Linux is using Wayland.
        # https://bugreports.qt.io/browse/QTBUG-34976?focusedCommentId=276038&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel
        # 
        # Use gnome-screenshot instead.
        # 27 Dec 24 - gnome screenshot sometimes does run ...
        #   Made us think there's something wrong with how things are executed ...
        # TODO refactor so we reuse some parts for non-whole screen screen grabing
        #
        # gnome-screenshot sometimes doesn't work with QtCore.QProcess for whatever reason ...
        # Use python subprocess instead: https://stackoverflow.com/questions/89228/how-do-i-execute-a-program-or-call-a-system-command

        scTool = 'gnome-screenshot'

        if platform.system() == "Linux":
            print("Linux detected. Note: require '{}' to work.".format(scTool))

            try:
                subprocess.run([scTool, '-f', picPath, '-d', str(int(timeDelay))])
            except subprocess.CalledProcessError:
                print("Error running {}".format(scTool))
                return None
            else:
                pixmap = QtGui.QPixmap()
                pixmap.load(picPath)
                return pixmap
        
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

    def getTempWholeScreen(self):
        return self.getWholeScreen("/tmp/screenshot_proceeder_screenbg.jpg")

    def getCroppedScreen(self, picPath, timeDelay, rect):
        pixmap = self.getWholeScreen(picPath, timeDelay)
        # TODO this doent save the new cropped version
        return pixmap.copy(rect)

    def getRepeatCroppedScreen(self, picPath, timeDelay, rect, key, totCount):
        self.stopRepeatScreenshot = False
        for count in range(totCount):
            if not self.stopRepeatScreenshot:
                self.getCroppedScreen(os.path.join(picPath, "{}.jpg".format(count)), timeDelay, rect)
                self.keyActuator.proceed(key)

    def stopRepeatCroppedScreen(self):
        # Note: NOT thread safe.
        self.stopRepeatScreenshot = True
