import xmltodict, json, os
from .codeclasses import *

def readxml(path):
    with open(path,"r") as xmlfile:
        xml = xmlfile.read()
        dict = xmltodict.parse(xml)
    return dict

def readjson(path):
    with open(path,"r") as jsonfile:
        jsond = jsonfile.read()
        jsond = jsond.replace(jsond.split("{")[0],"")
        listy = list(jsond)
        for i in range(1,3):
            listy[listy.__len__()-i] = ""

        jsond = ""
        for i in listy:
            jsond += i
        dict = json.loads(jsond)
    return dict

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
    d[k] = objectfromdict(Base, d[k])


def listparse(n,ogd,d):
    if d.__class__.__name__ == "dict" or d.__class__.__name__ == "OrderedDict":
        ogd[n].append(objectfromdict(Base,d))
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
        setattr(obj,removebadthings(k),d[k])
    return obj
