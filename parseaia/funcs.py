from .codeclasses import *
from .uiclasses import *
import os

global cname

def removebadthings(text:str):
    return text.replace("@","").replace("#","").replace("[","").replace("]","").replace("-","_").replace("$","").replace(" ","_")

def deletedir(fp):
    for file in os.listdir(fp):
        if os.path.isdir(f"{fp}/{file}"):
            deletedir(f"{fp}/{file}")
        else:
            os.remove(f"{fp}/{file}")
    os.rmdir(fp)

def dictionaryparse(k,d):
    exec(f"global cname\ncname = {removebadthings(k)}")
    d[k] = objectfromdict(cname, d[k])


def listparse(n,ogd,d):
    if d.__class__.__name__ == "dict" or d.__class__.__name__ == "OrderedDict":
        exec(f"global cname\ncname = {removebadthings(n)}")
        ogd[n].append(objectfromdict(cname,d))
    else:
        ogd[n].append(d)


def objectfromdict(c,d):
    # Usage: obj = objectfromdict(class,dictionary)
    obj = c()
    for k in d:
        if d[k].__class__.__name__ == "dict" or d[k].__class__.__name__ == "OrderedDict":
            dictionaryparse(k,d)
        elif d[k].__class__.__name__ == "list":
            l = d[k]
            d[k] = []
            for i in l:
                listparse(k,d,i)
        exec(f"obj.{removebadthings(k)} = d[k]")
    return obj


def getblocks(block):
    l = [block]
    if "next" in block.__dict__:
        l += getblocks(block.next.block)
    if "statement" in block.__dict__:
        l += getblocks(block.statement.block)
    if "value" in block.__dict__:
        if block.value.__class__.__name__ == "list":
            for i in block.value:
                l += getblocks(i.block)
        else:
            l += getblocks(block.value.block)

    return l


def blocktobetterblock(block):
    statechild = "statement" in block.__dict__
    nextchild = "next" in block.__dict__
    bb = betterblock()
    bb.rawself = block
    bb.type = block.type
    bb.id = block.id
    bb.top = False
    if "x" in block.__dict__:
        bb.x = int(block.x)
        bb.y = int(block.y)
        bb.top = True

    bb.children = []
    if statechild:
        bb.children.append(blocktobetterblock(block.statement.block))
    if nextchild:
        bb.children.append(blocktobetterblock(block.next.block))

    bb.values = []
    if "value" in block.__dict__:
        if block.value.__class__.__name__ == "list":
            for i in block.value:
                bb.values.append(blocktobetterblock(i.block))
        else:
            bb.values.append(blocktobetterblock(block.value.block))

    return bb
