class Base:
    pass


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
    rawself: Base
    name: str
    next = any

    def __init__(self,rawstatement:Base):
        self.rawself = rawstatement
        self.name = rawstatement.name
        self.child = rawstatement.block


class Value:
    rawself: Base
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
        self.rawself = raw
        self.name = raw.name


class Block:
    rawself: Base
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
        self.rawself = base
        self.type = base.type
        self.id = base.id

        # Position stuff
        if "x" in base.__dict__:
            self.x = int(base.x)
            self.y = int(base.y)
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
    xml: Base
    blockslist: [Block]
    gvars: [Block]
    events: [Block]
    procedures: [Block]
    blocks: [Block]
    blocksdict: {str:Block}