import subprocess
import platform
import glob
from pathlib import Path

def getNumericNameOrder(name):
    # Note: does not handle file name with non-numeric characters.
    return  int(Path(name).stem)

class Combiner():
    def run(self, quality, path):
        quality = round(quality)
        quality = quality if quality > 0 and quality <= 100 else (1 if quality <= 0 else 100)
        if platform.system() == "Linux":
            fileList = sorted(glob.glob("{}/*.jpg".format(path)), key=getNumericNameOrder)
            if not fileList:
                print("No expected file exists in the folder: '{}'".format(path))
            else:
                try:
                    subprocess.run(["magick"] + fileList + ["-quality", "{}".format(quality), "{}/outfile.pdf".format(path)])
                except subprocess.CalledProcessError:
                    print("Error converting to PDF using the images in ".format(path))
                    return None
        else:
            raise NotImplementedError("Only support Linux (Fedora Gnome)")

