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
    rawsself: statement
    name: str
    child = any  # betterblock


class betterblock:
    rawself: block
    type: str
    id: str
    x: int
    y: int
    statement: betterstatement
    children: list  # betterblock
    values: list  # betterblock
    top: bool


