from .codeclasses import Code
from .uiclasses import UI
from .funcs import objectfromdict, getblocks, blocktobetterblock, deletedir
from .todict import readxml, readjson
import os
import zipfile


class Screen():  # Usage: Project("path/to/my/project.aia")
    Code: Code
    UI: UI

    def __init__(self, fp, scrname, tempfolderfp="parseaiatemp"):
        if not os.path.isdir(tempfolderfp):
            os.mkdir(tempfolderfp)
        else:
            deletedir(tempfolderfp)
            os.mkdir(tempfolderfp)

        with zipfile.PyZipFile(fp) as zipf:
            zipf.extractall(tempfolderfp)

        self.getcode(scrname, tempfolderfp)
        self.getUI(scrname, tempfolderfp)

        deletedir(tempfolderfp)


    def getUI(self,scrname,tempfolderfp):
        uipath = f"{tempfolderfp}/src/appinventor/"
        for i in range(2):
            uipath += os.listdir(uipath)[0] + "/"

        uipath += scrname + ".scm"
        d = readjson(uipath)

        self.UI = objectfromdict(UI,d)



    def getcode(self, scrname,tempfolderfp):
        blockpath = f"{tempfolderfp}/src/appinventor/"
        for i in range(2):
            blockpath += os.listdir(blockpath)[0] + "/"

        blockpath += scrname + ".bky"
        d = readxml(blockpath)
        self.Code = objectfromdict(Code, d)

        topblocks = self.Code.xml.block
        self.Code.gvars = []
        self.Code.events = []
        self.Code.procedures = []
        self.Code.blockslist = []
        self.Code.blocks = []
        if topblocks.__class__.__name__ != "list":
            topblocks = [topblocks]
        for i in topblocks:
            if i.type == "component_event":
                self.Code.events.append(i)
            elif i.type == "global_declaration":
                self.Code.gvars.append(i)
            elif i.type == "procedures_defnoreturn":
                self.Code.procedures.append(i)

            self.Code.blocks.append(blocktobetterblock(i))
            self.Code.blockslist += getblocks(i)



        self.Code.blocksdict = {}
        for i in self.Code.blockslist:
            if i.type in self.Code.blocksdict:
                self.Code.blocksdict[i.type].append(i)
            else:
                self.Code.blocksdict[i.type] = [i]



