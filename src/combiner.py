import subprocess
import platform

class Combiner():
    def run(path, quality):
        quality = round(quality)
        quality = quality if quality > 0 and quality <= 100 else (1 if quality <= 0 else 100)
        if platform.system() == "Linux":
            try:
                subprocess.run("magick $(ls {}/*.jpg | sort -n) -quality {} outfile.pdf".format(path, quality).split())
            except subprocess.CalledProcessError:
                print("Error converting to PDF using the images in ".format(path))
                return None
        else:
            raise NotImplementedError("Only support Linux (Fedora Gnome)")