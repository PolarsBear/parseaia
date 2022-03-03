import os
from .otherclasses import Font
from .otherclasses import Audio
from PIL import Image

import logging

logger = logging.getLogger(__name__)


def list_blocks(block):
    gathered_blocks = [block]
    if "next" in block.__dict__:
        if "next" in block.__dict__:
            gathered_blocks += list_blocks(block.next)
    if "statements" in block.__dict__:
        for state in block.statements:
            if "next" in state.__dict__:
                gathered_blocks += list_blocks(state.next)
    if "values" in block.__dict__:
        for val in block.values:
            gathered_blocks += list_blocks(val)
    return gathered_blocks


def delete_dir(fp):
    for file in os.listdir(fp):
        if os.path.isdir(f"{fp}/{file}"):
            delete_dir(f"{fp}/{file}")
        else:
            os.remove(f"{fp}/{file}")
    os.rmdir(fp)


def assetparse(obj, assetpath, filename):
    path = assetpath + filename
    if not os.path.isdir(path):
        try:
            # Madness for disconnecting image from file
            tmp = Image.open(fp=path)
            tmp2 = Image.frombytes(tmp.mode, tmp.size, tmp.tobytes())
            tmp.close()
            tmp2.filename = filename
            obj.images.append(tmp2)
        except:
            if filename.endswith("ttf") or filename.endswith("pil"):
                # Is a font
                obj.fonts.append(Font(path, filename))
            elif filename.endswith("wav") or filename.endswith("mp3"):
                # Is an audio file
                logger.debug('Audio full filename: %s', path)
                obj.audio.append(Audio(path, filename))
            else:
                # Not Image, Font or Audio, assuming it is text
                with open(path, "r", encoding="UTF-8") as asset:
                    obj.assets[filename] = asset.read()

            # This is an if else nightmare, I wish python had a switch keyword
