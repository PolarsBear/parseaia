class Components:
    Name: str
    Type: str
    Version: int
    Uuid: int


class Properties:
    Name: str
    Type: str
    Version: int
    AppName: str
    Title: str
    Uuid: int
    Components: [Components]


class UI:
    authURL: [str]
    YaVersion: int
    Source: str
    Properties: Properties