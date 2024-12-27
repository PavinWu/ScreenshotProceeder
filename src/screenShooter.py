from PySide6 import QtCore, QtWidgets, QtGui
import platform
import os
import subprocess
import time

class ScreenShooter(QtWidgets.QWidget):
    def __init__(self, keyActuator):
        super().__init__()
        self.keyActuator = keyActuator
        self.doStopRepeatScreenshot = False

    def getWholeScreen(self, picPath):
        # Note: The Qt's screen grabber doesn't work on Wayland. Assume Linux is using Wayland.
        # https://bugreports.qt.io/browse/QTBUG-34976?focusedCommentId=276038&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel
        # 
        # Use gnome-screenshot instead.
        # 27 Dec 24 - gnome screenshot sometimes does run ...
        #   Made us think there's something wrong with how things are executed ...
        # Later: gnome-screenshot sometimes doesn't work with QtCore.QProcess for whatever reason ...
        # Use python subprocess instead: https://stackoverflow.com/questions/89228/how-do-i-execute-a-program-or-call-a-system-command

        scTool = 'gnome-screenshot'

        if platform.system() == "Linux":
            try:
                subprocess.run([scTool, '-f', picPath])
            except subprocess.CalledProcessError:
                print("Error running {}".format(scTool))
                return None
            else:
                pixmap = QtGui.QPixmap()
                pixmap.load(picPath)
                return pixmap
        else:
            raise NotImplementedError("Only support Linux (Fedora Gnome)")
        
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

    def getCroppedScreen(self, picPath, rect):
        pixmap = self.getTempWholeScreen()
        croppedPixmap = pixmap.copy(rect)
        croppedPixmap.save(picPath)
        return croppedPixmap

    def getRepeatCroppedScreen(self, appSelectWait_s, picPath, timeDelay_s, rect, key, totCount):
        self.doStopRepeatScreenshot = False

        # App selection wait
        print("Waiting for user to select application...")
        self.__countDown__(appSelectWait_s)

        # Proceed and take screenshots
        for count in range(totCount):
            if count > 0 and not self.doStopRepeatScreenshot:
                self.keyActuator.proceed(key)
            print("Waiting to take screenshot {}".format(count))
            self.__countDown__(timeDelay_s)
            print("Taking screenshot {}".format(count))
            
            if not self.doStopRepeatScreenshot:
                self.getCroppedScreen(os.path.join(picPath, "{}.jpg".format(count)), rect)

    def stopRepeatCroppedScreen(self):
        # Note: NOT thread safe. Assume this is the only function setting stopRepeatScreenshot to true.
        self.doStopRepeatScreenshot = True
        print("Stop taking screenshots")

    def isStopRepeatScreenshot(self):
        return self.doStopRepeatScreenshot

    def __countDown__(self, totalDur_s):
        timeDelta = 0.5
        timeLeft = totalDur_s
        print("Time left (s): ", end = "")
        while timeLeft > 0 and not self.doStopRepeatScreenshot:
            time.sleep(timeDelta)
            timeLeft -= timeDelta
            
            print("{}".format(timeLeft))    
