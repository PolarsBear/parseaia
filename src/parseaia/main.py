from .codeclasses import Code, Block
from .uiclasses import UI
from .funcs import listBlocks, deletedir
from .dictionaryutils import readxml, readjson, objectfromdict
import os, zipfile
from PIL import Image
from time import sleep


class Screen:  # Usage: Project("path/to/my/project.aia")
    Code: Code
    UI: UI

    def __init__(self, scrname, dir):

        self.getCode(scrname, dir)
        self.getUI(scrname, dir)

    def getUI(self, scrname, dir):
        dir += scrname + ".scm"
        d = readjson(dir)
        self.UI = UI(d)

    def getCode(self, scrname, dir):
        dir += scrname + ".bky"
        d = readxml(dir)
        self.Code = objectfromdict(Code, d)

        rawblocks = self.Code.xml.block
        self.Code.gvars = []
        self.Code.events = []
        self.Code.procedures = []
        self.Code.blockslist = []
        self.Code.blocks = []


        if rawblocks.__class__.__name__ != "list":
            rawblocks = [rawblocks]
        for i in rawblocks:
            self.Code.blocks.append(Block(i))

        for i in self.Code.blocks:
            self.Code.blockslist += listBlocks(i)

        self.Code.blocksdict = {}
        for i in self.Code.blockslist:
            if i.type in self.Code.blocksdict:
                self.Code.blocksdict[i.type].append(i)
            else:
                self.Code.blocksdict[i.type] = [i]

            # Create Lists of top level blocks
            if i.type == "component_event":
                self.Code.events.append(i)
            elif i.type == "global_declaration":
                self.Code.gvars.append(i)
            elif i.type == "procedures_defnoreturn":
                self.Code.procedures.append(i)


class Project:
    screens: [Screen]
    images: [Image.Image]
    assets: {str:str}

    def __init__(self, fp, tempfolderfp="parseaiatemp"):
        self.screens = []
        self.images = []
        self.assets = {}
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
                scr = Screen(i.replace(".bky", "", 1), dir)
                self.__setattr__(i.replace(".bky", "", 1), scr)
                self.screens.append(scr)

        self.getAssets(tempfolderfp)

        deletedir(tempfolderfp)

    def getAssets(self, dir):
        path = dir + "/assets/"
        for i in os.listdir(path):
            if not os.path.isdir(path + i):
                try:
                    # Madness for disconnecting image from file
                    tmp = Image.open(fp=path + i)
                    tmp2 = Image.frombytes(tmp.mode,tmp.size,tmp.tobytes())
                    tmp.close()
                    tmp2.filename = i
                    self.images.append(tmp2)

                except:
                    # Not Image, read text
                    with open(path+i,"r") as asset:
                        self.assets[i] = asset.read()

