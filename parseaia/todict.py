import xmltodict, json
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
