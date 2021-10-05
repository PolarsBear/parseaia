from .dictionaryutils import objectfromdict
from .codeclasses import Base


class Component:
    rawself: Base
    Name: str
    Type: str
    Version: int
    Uuid: int

    def __init__(self, raw:Base):
        self.rawself = raw

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
    rawself: Base
    Name: str
    Type: str
    Version: int
    AppName: str
    Title: str
    Uuid: int
    Components: [Component]

    def __init__(self,raw:Base):
        self.rawself = raw

        for i in raw.__dict__:
            self.__setattr__(i,raw.__getattribute__(i))

        # Add Components
        if "Components" in raw.__dict__:
            self.Components = []
            if raw.Components.__class__.__name__ != "list":
                raw.Components = [raw.Components]

            for component in raw.Components:
                self.Components.append(Component(component))



class UI:
    rawself: Base
    authURL: [str]
    YaVersion: int
    Source: str
    Properties: Properties

    def __init__(self,d:dict):
        self.rawself = objectfromdict(Base,d)
        for i in self.rawself.__dict__:
            self.__setattr__(i,self.rawself.__getattribute__(i))

        # Add Properties
        self.Properties = Properties(self.rawself.Properties)