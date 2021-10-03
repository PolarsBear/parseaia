from .codeclasses import Code
from .uiclasses import UI
from .funcs import objectfromdict, getblocks, blocktobetterblock, deletedir
from .todict import readxml, readjson
import os
import zipfile

class Screen:  # Usage: Project("path/to/my/project.aia")
    Code: Code
    UI: UI

    def __init__(self, scrname, dir):

        self.getcode(scrname, dir)
        self.getUI(scrname, dir)




    def getUI(self,scrname,dir):
        dir += scrname + ".scm"
        d = readjson(dir)
        self.UI = objectfromdict(UI,d)



    def getcode(self, scrname,dir):
        dir += scrname + ".bky"
        d = readxml(dir)
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


class Project:
    def __init__(self,fp,tempfolderfp="parseaiatemp"):
        self.screens = []
        if not os.path.isdir(tempfolderfp):
            os.mkdir(tempfolderfp)
        else:
            deletedir(tempfolderfp)
            os.mkdir(tempfolderfp)

        with zipfile.PyZipFile(fp) as zipf:
            zipf.extractall(tempfolderfp)

        d1 = os.listdir(f"{tempfolderfp}/src/appinventor")[0]
        d2 = os.listdir(f"{tempfolderfp}/src/appinventor/{d1}")[0]
        dir = f"{tempfolderfp}/src/appinventor/{d1}/{d2}/"
        for i in os.listdir(dir):
            if i.endswith(".bky"):
                scr = Screen(i.replace(".bky","",1),dir)
                self.__setattr__(i.replace(".bky","",1),scr)
                self.screens.append(scr)

        deletedir(tempfolderfp)