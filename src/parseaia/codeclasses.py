class localname:
    name: str


class mutation:
    component_type: str
    is_generic: str
    instance_name: str
    event_name: str
    localname: localname


class field:
    name: str
    text: str


class value:
    name: str
    block: any  # block


class eventparam:
    name: str


class arg:
    name:str


class next:
    block: any  # block


class statement:
    name: str
    block: any  # block


class block:
    type: str
    id: str
    x: str
    y: str
    next: next
    statement: statement
    field: field
    value: value or list


class yacodeblocks:
    ya_version: str
    language_version: str


class xml:
    xmlns: str
    block: list
    yacodeblocks: yacodeblocks


class Code:
    xml: xml
    blockslist: list
    gvars: list
    events: list
    procedures: list
    blocks: list
    blocksdict: dict


class betterstatement:
    rawself: statement
    name: str
    next = any  # betterblock

    def __init__(self,rawstatement:statement):
        self.rawself = rawstatement
        self.name = rawstatement.name
        self.child = rawstatement.block


class bettervalue:
    rawself: value
    name: str
    type: str
    id: str
    x: int
    y: int
    statements: [betterstatement]
    next: any
    values: list  # betterblock
    top: bool

    def __init__(self,raw:value,block):
        for i in block.__dict__:
            self.__setattr__(i,block.__getattribute__(i))
        self.rawself = raw
        self.name = raw.name


class betterblock:
    rawself: block
    type: str
    id: str
    x: int
    y: int
    statements: [betterstatement]
    next: any
    values: [bettervalue]  # betterblock
    top: bool


