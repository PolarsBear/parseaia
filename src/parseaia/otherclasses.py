import os

import mutagen
from PIL import ImageFont
from mutagen import File

import logging

logger = logging.getLogger(__name__)


class Base:
    pass


class Asset:
    filename: str


class TextAsset(Asset):
    data: str

    def __init__(self, filepath, filename):
        self.filename = filename
        with open(filepath, "r", encoding="UTF-8") as file:
            self.data = file.read()


class Font(Asset):
    contents: bytes

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
class Audio(Asset):
    _data = mutagen.FileType
    sample_rate: int
    duration: float
    channels: int
    samples: int

    def __init__(self, filepath, filename):
        self.filename = filename
        self._data = File(filepath)  # Turns out mutagen is just way better than librosa
        self.duration = self._data.info.length
        self.channels = self._data.info.channels
        self.sample_rate = self._data.info.sample_rate
        self.samples = round(self.duration * self.sample_rate)  # Don't know if this is actually correct, but oh well
        # TODO: add graphing functionality? potentially a function to play the sound?


class Video(Asset):
    _data = mutagen.FileType
    sample_rate: int
    duration: float
    audio_channels: int
    samples: int

    def __init__(self, filepath, filename):
        self.filename = filename
        self._data = File(filepath)
        self.duration = self._data.info.length
        self.audio_channels = self._data.info.channels
        self.sample_rate = self._data.info.sample_rate
        self.samples = round(self.duration * self.sample_rate)  # Don't know if this is actually correct, but oh well


class Binary(Asset):
    data: bytes

    def __init__(self, filepath, filename):
        self.filename = filename
        with open(filepath, "rb") as file:
            self.data = file.read()
