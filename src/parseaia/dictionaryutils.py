import xmltodict, json, os
from .otherclasses import *


def readxml(path):
    with open(path,"r", encoding="utf-8") as xmlfile:
        xml = xmlfile.read()
        try:
            dict = xmltodict.parse(xml)
        except xmltodict.expat.ExpatError:
            tmp = Base()
            tmp.nothing = True
            return {"xml":tmp}
    return dict


def readjson(path):
    with open(path,"r", encoding="utf-8") as jsonfile:
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


def objectfromdict(c,d):
    # Usage: obj = objectfromdict(class,dictionary)
    obj = c()
    for k in d:
        if d[k].__class__.__name__ == "dict" or d[k].__class__.__name__ == "OrderedDict":
            d[k] = objectfromdict(Base, d[k])
        elif d[k].__class__.__name__ == "list":
            l = d[k]
            d[k] = []
            for i in l:
                if i.__class__.__name__ == "dict" or i.__class__.__name__ == "OrderedDict":
                    d[k].append(objectfromdict(Base, i))
                else:
                    d[k].append(i)
        setattr(obj,removebadthings(k),d[k])
    return obj
