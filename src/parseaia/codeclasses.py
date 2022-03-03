from .funcs import list_blocks
from .otherclasses import Base
from .dictionaryutils import objectfromdict

class Field:
    name: str
    text: str

    def __init__(self,raw:Base):
        self.name = raw.name
        if "text" in raw.__dict__:
            self.text = raw.text
        else:
            self.text = None


class Statement:
    name: str
    next = any

    def __init__(self,rawstatement:Base):
        self.name = rawstatement.name
        self.child = rawstatement.block


class Value:
    name: str
    type: str
    id: str
    x: int
    y: int
    statements: [Statement]
    next: any
    values: list
    top: bool

    def __init__(self,raw:Base,block):
        for i in block.__dict__:
            self.__setattr__(i,block.__getattribute__(i))
        self.name = raw.name


class Block:
    type: str
    id: str
    x: int
    y: int
    statements: [Statement]
    next: any
    values: [Value]
    fields: [Field]
    top: bool

    def __init__(self,base:Base):
        if "block" in base.__dict__:
            base = base.block
        self.type = base.type
        self.id = base.id

        # Position stuff
        if "x" in base.__dict__:
            try:
                self.x = int(base.x)
                self.y = int(base.y)
            except ValueError:
                print(f'\033[31mAlert: block of type "{self.type}" with id of "{self.id}" has unexpected x and y values of "{base.x}" and "{base.y}" respectively. Something is VERY wrong!\033[39m')
            self.top = True
        else:
            self.top = False
            self.x = None
            self.y = None

        # Add Statements
        if "statement" in base.__dict__:
            if base.statement.__class__.__name__ != "list":
                self.statements = [Statement(base.statement)]
            else:
                self.statements = []
                for state in base.statement:
                    self.statements.append(Statement(state))

        # Add Next
        if "next" in base.__dict__:
            self.next = Block(base.next)

        # Add Values
        if "value" in base.__dict__:
            if base.value.__class__.__name__ != "list":
                self.values = [Value(base.value,Block(base.value.block))]
            else:
                self.values = []
                for val in base.value:
                    self.values.append(Value(val,Block(val.block)))

        # Add properties from mutations
        if "mutation" in base.__dict__:
            for k in base.mutation.__dict__:
                self.__setattr__(k, base.mutation.__getattribute__(k))


        if "field" in base.__dict__:
            if base.field.__class__.__name__ != "list":
                base.field = [base.field]
            self.fields = []
            for i in base.field:
                self.fields.append(Field(i))


class Code:
    yacodeblocks: Base
    xmlns: str
    blockslist: [Block]
    global_vars: [Block]
    events: [Block]
    procedures: [Block]
    blocks: [Block]
    blocksdict: {str:Block}

    def __init__(self, dictionary, scrname):
        rawself = objectfromdict(Base, dictionary)
        if "block" not in rawself.xml.__dict__:
            if "nothing" in rawself.xml.__dict__:
                print(f"\033[31mAlert: Screen {scrname} has NOTHING in its code XML. Something might be wrong...\033[39m")
                delattr(rawself.xml,"nothing")
            else:
                print(f"\033[33mAlert: Screen {scrname} has no code. Something might be wrong...\033[39m")
        for i in rawself.xml.__dict__:
            if i != "block":
                self.__setattr__(i,rawself.xml.__getattribute__(i))

        self.global_vars = []
        self.events = []
        self.procedures = []
        self.blockslist = []
        self.blocks = []

        if "block" not in rawself.xml.__dict__:
            return
        rawblocks = rawself.xml.block

        if rawblocks.__class__.__name__ != "list":
            rawblocks = [rawblocks]
        for i in rawblocks:
            self.blocks.append(Block(i))

        for i in self.blocks:
            self.blockslist += list_blocks(i)

        self.blocksdict = {}
        for i in self.blockslist:
            if i.type in self.blocksdict:
                self.blocksdict[i.type].append(i)
            else:
                self.blocksdict[i.type] = [i]

            # Create Lists of top level blocks
            if i.type == "component_event":
                self.events.append(i)
            elif i.type == "global_declaration":
                self.global_vars.append(i)
            elif i.type == "procedures_defnoreturn":
                self.procedures.append(i)