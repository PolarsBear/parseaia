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
    child = any  # betterblock

    def __init__(self,rawstatement:statement):
        self.rawself = rawstatement
        self.name = rawstatement.name
        self.child = rawstatement.block


class betterblock:
    rawself: block
    type: str
    id: str
    x: int
    y: int
    statements: [betterstatement]
    children: list  # betterblock
    values: list  # betterblock
    top: bool


