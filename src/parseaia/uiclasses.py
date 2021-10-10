from .dictionaryutils import objectfromdict
from .otherclasses import Base


class Component:
    Name: str
    Type: str
    Version: int
    Uuid: int

    def __init__(self, raw:Base):

        for i in raw.__dict__:
            self.__setattr__(i,raw.__getattribute__(i))

        # Add Components
        if "Components" in raw.__dict__:
            self.Components = []
            if raw.Components.__class__.__name__ != "list":
                raw.Components = [raw.Components]

            for component in raw.Components:
                self.Components.append(Component(component))



class Properties:
    Name: str
    Type: str
    Version: int
    AppName: str
    Title: str
    Uuid: int
    Components: [Component]

    def __init__(self,raw:Base):
        for i in raw.__dict__:
            self.__setattr__(i,raw.__getattribute__(i))

        self.Components = []
        # Add Components
        if "Components" in raw.__dict__:
            if raw.Components.__class__.__name__ != "list":
                raw.Components = [raw.Components]

            for component in raw.Components:
                self.Components.append(Component(component))
        else:
            print(f"\033[33mAlert: {self.Name} has no ui elements. Something might be wrong...\033[39m")



class UI:
    authURL: [str]
    YaVersion: int
    Source: str
    Properties: Properties

    def __init__(self,d:dict):
        rawself = objectfromdict(Base,d)
        for i in rawself.__dict__:
            self.__setattr__(i,rawself.__getattribute__(i))

        # Add Properties
        self.Properties = Properties(rawself.Properties)