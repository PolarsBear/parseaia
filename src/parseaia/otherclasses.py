import os

import numpy
from PIL import ImageFont
import librosa
# librosa doesn't depend on any external tools (other than ffmpeg for some operations)
# TODO: catch librosa's annoying "UserWarning: PySoundFile failed." error
from soundfile import available_formats as av_fo

import logging
logger = logging.getLogger(__name__)


logger.info(f"Available audio formats are: {av_fo()} (without FFMPEG) And, like, absolutely everything with FFMPEG")


class Base:
    pass


class Font:
    def __init__(self, filepath, filename):
        self.filename = filename
        with open(filepath, "rb") as fontfile:
            self.contents = fontfile.read()

    def make_image_font(self, tmpfilename="tmpfont"):
        iterator = 0
        ogtmpfilename = tmpfilename
        while os.path.exists(tmpfilename):
            tmpfilename = ogtmpfilename + str(iterator)
            iterator += 1
        with open(tmpfilename, "wb") as fontfile:
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
    filename: str
    _data = numpy.ndarray
    sampling_rate: int
    duration: float
    channels: int
    samples: int

    def __init__(self, filepath, filename):
        self.filename = filename
        self._data, self.sampling_rate = librosa.load(filepath, mono=False)
        # For some reason librosa has the "convert to mono" option True by default, so we have to disable it manually
        self.duration = librosa.get_duration(filename=filepath)
        self.channels = self._data.shape[0] if len(self._data.shape) > 1 else 1
        self.samples = self._data.shape[1] if self.channels > 1 else self._data.shape[0]
        # TODO: add graphing functionality? potentially a function to play the sound?


