import os
import zipfile
import logging

from PIL import Image

from .codeclasses import Code
from .dictionaryutils import readxml, readjson
from .funcs import delete_dir, assetparse
from .otherclasses import Font, Audio
from .uiclasses import UI

logger = logging.getLogger(__name__)


class Screen:  # Usage: Project("path/to/my/project.aia")
    Code: Code
    UI: UI

    def __init__(self, scrname, dir):
        dir1, dir2 = dir, dir

        # Code
        dir1 += scrname + ".bky"
        d = readxml(dir1)
        self.Code = Code(d, scrname)

        # UI
        dir2 += scrname + ".scm"
        d = readjson(dir2)
        self.UI = UI(d)


class Project:
    screens: [Screen]
    images: [Image.Image]
    audio: [Audio]
    fonts: [Font]
    assets: {str: str}
    parse_function: any  # Function that can be set as a way for other parsing methods to be available if need be

    def __init__(self, fp, tempfp="parseaiatemp", parse_function=assetparse):
        self.parse_function = parse_function
        self.tempfp = tempfp
        self.screens = []
        self.images = []
        self.fonts = []
        self.audio = []
        self.assets = {}
        if not os.path.isdir(tempfp):
            os.mkdir(tempfp)
        else:
            delete_dir(tempfp)
            os.mkdir(tempfp)

        with zipfile.PyZipFile(fp) as zipf:
            zipf.extractall(tempfp)

        d1 = os.listdir(f"{tempfp}/src/appinventor")[0]
        d2 = os.listdir(f"{tempfp}/src/appinventor/{d1}")[0]
        dir = f"{tempfp}/src/appinventor/{d1}/{d2}/"
        for i in os.listdir(dir):
            if i.endswith(".bky"):
                scr = Screen(i.replace(".bky", "", 1), dir)
                self.__setattr__(i.replace(".bky", "", 1), scr)
                self.screens.append(scr)

        # Get assets
        assetpath = tempfp + "/assets/"
        if not os.path.exists(assetpath):
            return
        if "parse_function" in self.__dict__:
            if self.parse_function.__code__.co_argcount != 3:
                print(
                    f'''\033[31mAlert: parse_function "{self.parse_function.__name__}" has {"less" if self.parse_function.__code__.co_argcount < 3 else "more"} than 3 arguments. It won't be called!\033[39m''')
        for i in os.listdir(assetpath):
            if self.parse_function.__code__.co_argcount == 3:  # Checking if parse function has 3 arguments (self, assetpath, filename)
                self.parse_function(self, assetpath, i)

        # Delete temp folder and contents
        delete_dir(tempfp)
