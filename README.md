# Parse .AIA
This is a simple python library for parsing the contents of .AIA files ([App Inventor](https://appinventor.mit.edu/) Projects).

# Basic Explanation
The only class you need for this library is parseaia.Screen, it represents one screen in a project, with code blocks and ui.

parseaia.Screen takes two arguments for its init function: the file path to the .aia, and the name of the screen.
In future updates, I might change this to automatically find all screens in a project.

## Tiny Example:
```py
import parseaia 
screen = parseaia.Screen("myproject.aia", "ScreenName") # Getting the screen from the .aia

for i in screen1.UI.Properties.Components: # Looping through all UI components
    print(i.Name) # Outputting all the UI components' names
```
Output:
```
Label1
Button1
Notifier1
Clock1
```
In my project, I had these UI components, with these names.

# Documentation (kinda scuffed)

## The `Screen` class

### The Init
Arguments:
fp: str | .aia filepath

scrname: str | Name of the screen, in the project

tempfolderfp = "parseaiatemp": str | Keyword argument, defines the name of the temp folder used by the library to unzip the .aia

### Properties
Code: [`Code`](https://github.com/PolarsBear/parseaia/blob/main/README.md#the-code-class) | holds all the information on the code blocks in the screen

UI: [`UI`](https://github.com/PolarsBear/parseaia/blob/main/README.md#the-ui-class) | holds all the information on the UI components in the screen

## The `Code` class

### Properties
xml: xml | an object that is simply the original xml in the form of an object, not suggested

blocks: [[`block`](https://github.com/PolarsBear/parseaia/blob/main/README.md#the-code-block-class)] | a list, the top of the hierarchy of [`blocks`], all the events, global variable declarations, and procedure definitions

events: [[`block`](https://github.com/PolarsBear/parseaia/blob/main/README.md#the-code-block-class)] | a list of the event [`blocks`](https://github.com/PolarsBear/parseaia/blob/main/README.md#the-code-block-class)

gvars: [[`block`](https://github.com/PolarsBear/parseaia/blob/main/README.md#the-code-block-class)] | a list of the global variable declarations

procedures: [[`block`](https://github.com/PolarsBear/parseaia/blob/main/README.md#the-code-block-class)] | a list of procedure definitions

blockslist: [[`block`](https://github.com/PolarsBear/parseaia/blob/main/README.md#the-code-block-class)] | a list of all [`blocks`](https://github.com/PolarsBear/parseaia/blob/main/README.md#the-code-block-class), without any regard for hierarchy

blocksdict: {str:[[`block`](https://github.com/PolarsBear/parseaia/blob/main/README.md#the-code-block-class)]} a dictionary of all [`blocks`](https://github.com/PolarsBear/parseaia/blob/main/README.md#the-code-block-class), each key is a type of [`block`](https://github.com/PolarsBear/parseaia/blob/main/README.md#the-code-block-class), with the list of all [`blocks`](https://github.com/PolarsBear/parseaia/blob/main/README.md#the-code-block-class) of that type as its value

## The `UI` class

### Properties
authURL: [str] | for authentication. But authentication for what?

YaVersion: str | version of "Ya", whatever that may be

Source: str | Don't ask me! I dunno what this does.

Properties: [`Properties`](https://github.com/PolarsBear/parseaia/blob/main/README.md#the-ui-properties-class) | contains all properties of the UI, and is the gateway into actual UI stuff, like the [`components`](https://github.com/PolarsBear/parseaia/blob/main/README.md#the-ui-component-class)

## The code `Block` class
This class is not actually called `Block`, but instead `betterblock`, since most classes are actually just ripped straight out of the xml/json, and inside of the xml, there was something named `block`

### Properties
rawself: block | actual xml ripped block, minor changes, but I dare say mine is better

type: str | type of block

id: str | unique id

x: int | x coords in block editor

y: int | y coords in block editor

statement: betterstatement | IF, FOR, WHILE statements and such

children: betterblock | Children of the block

values: betterblock | Values attached to the block

top: bool | If or not the block is toplevel

## The UI `Properties` class
Again, most of this stuff is ripped straight outta xml/json, cuz I'm lazy, that's why this is kinda confusing
### Properties
Name: str | Name of the screen

Type: str | Type of component, but since this is a screen, it's always "Form"

Version: str | Version... of something

AppName: str | Name of the app

Title: str | Title of the screen

Uuid: str | Unique Id of the screen

Components: [`Component`](https://github.com/PolarsBear/parseaia/blob/main/README.md#the-ui-component-class)

## The UI `Component` class
Actually called `Components` cuz ripped out of json blah blah blah you know the drill

### Properties
Name: str | Name of the component
Type: str | Type of component
Version: str | Version of the component
Uuid: str | Unique id of the component

There will be more properties for the other unique properties of components, like Text, Color, and such
