import os
from PIL import ImageFont
import audiofile
# audiofile needs the external tool "sox". Not the best option. It'd be better
# to rely only on builtin functions or modules. For wav files, Python has 
# builtins, the problem is with mp3, flac, ogg.

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
        # TODO: check .otf files, too?

# Hold info about audio assets. At the moment, not interested in the
# content of the audio file, only checking if it looks valid
class Audio:
    def __init__(self,filepath,filename):
        self.filename = filename
        self.channels = audiofile.channels(filepath)
        self.samples = audiofile.samples(filepath)
        self.sampling_rate = audiofile.sampling_rate(filepath)
