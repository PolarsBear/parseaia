import os
from PIL import ImageFont


class Base:
    pass


class Font:
    def __init__(self,filepath,filename):
        self.filename = filename
        with open(filepath,"rb") as fontfile:
            self.contents = fontfile.read()

    def makeImageFont(self,tmpfilename="tmpfont"):
        iterator = 0
        ogtmpfilename = tmpfilename
        while os.path.exists(tmpfilename):
            tmpfilename = ogtmpfilename + str(iterator)
            iterator += 1
        self.newfilename = tmpfilename
        with open(tmpfilename,"wb") as fontfile:
            fontfile.write(self.contents)

        if self.filename.endswith(".ttf"):
            tmp = ImageFont.truetype(tmpfilename)
            return tmp
        elif self.filename.endswith(".pil"):
            tmp = ImageFont.load(tmpfilename)
            return tmp