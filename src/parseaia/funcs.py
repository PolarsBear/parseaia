import os
from PIL import Image, ImageFont

def listBlocks(block):
    gathered_blocks = [block]
    if "next" in block.__dict__:
        if "next" in block.__dict__:
            gathered_blocks += listBlocks(block.next)
    if "statements" in block.__dict__:
        for state in block.statements:
            if "next" in state.__dict__:
                gathered_blocks += listBlocks(state.next)
    if "values" in block.__dict__:
        for val in block.values:
            gathered_blocks += listBlocks(val)
    return gathered_blocks

def deletedir(fp):
    for file in os.listdir(fp):
        if os.path.isdir(f"{fp}/{file}"):
            deletedir(f"{fp}/{file}")
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
            if filename.endswith(".ttf"):
                tmp = ImageFont.truetype(path)
                tmp.filename = filename
                obj.fonts.append(tmp)
            elif filename.endswith(".pil"):
                tmp = ImageFont.load(path)
                tmp.filename = filename
                obj.fonts.append(tmp)
            else:
                # Not Image or Font, read text
                with open(path, "r", encoding="UTF-8") as asset:
                    obj.assets[filename] = asset.read()