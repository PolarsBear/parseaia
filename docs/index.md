# ParseAIA Documentation

ParseAIA is a simple python library for extracting data from .aia files ([App Inventor](https://appinventor.mit.edu/) projects)

## Simple explanation
The library works by extracting all of the data from an app inventor project. The one class you'll need is [`Project`](#class-project), it represents one app inventor project.

#### Quick Example:
```python
from parseaia import Project

myProject = Project("ExampleApp.aia") # Initiate a Project with the filepath to the .aia

print(myProject.Screen1.UI.Properties.Components) # Printing out all the UI elements
```
This example prints out all the UI elements in the screen "Screen1" (The default screen name when you create an app in app inventor, most apps will have it)

## Full Documentation

### *class* **Project**

##### Description
Every [`Screen`](#class-mainscreen) in the project is a property of this class, so if your project has a screen called "Screen1" then you can reference it with `Project.Screen1`

##### Properties
* screens: [`[Screen]`](#class-mainscreen) A list of screens, each holding its own [`Code`](#class-codeclassescode) and [`UI`](#class-uiclassesui)
* images: [`[PIL.Image.Image]`](https://pillow.readthedocs.io/en/stable/reference/Image.html#the-image-class) A list of all the images extracted from the project, on top of all the properties from Pillow, they also have `filename`, which is their original filename, as a string
* assets: `{str:str}` A dictionary of all the non-image assets, the keys are the filenames, and the values are the text in their files
* parse_function: `function` Used for extracting assets from the .aia, can be customised

### *class* main.**Screen**

##### Description
This is a screen from the [`Project`](#class-project), it has the screen's code and ui

##### Properties
* Code: [`Code`](#class-codeclassescode) The screen's code
* UI: [`UI`](#class-uiclassesui) The screen's UI

### *class* codeclasses.**Code**

##### Description
This is all of the code from a [`screen`](#class-mainscreen)

##### Properties
* rawself: `codeclasses.Base` Just the xml in object form, doesn't serve any purpose
* xml: `codeclasses.Base` Just the xml in object form, but this holds a bit of extra data I haven't transferred yet
* blockslist [`[Block]`](#class-codeclassesblock) A list of all blocks in the [`Screen`](#class-mainscreen), without any sense of hierarchy
* gvars [`[Block]`](#class-codeclassesblock) A list of all global variable declarations
* events [`[Block]`](#class-codeclassesblock) A list of all event handlers
* procedures [`[Block]`](#class-codeclassesblock) A list of all procedure definitions
* blocks [`[Block]`](#class-codeclassesblock) A list of the blocks in the top of the hierarchy (event handlers, global variable declarations, procedure definitions)
* blocksdict ```[str:[```[`Block`](#class-codeclassesblock)```]}``` A dictionary of all blocks, the key is the type of block, and the value is a list of blocks of that type

### *class* codeclasses.**Block**

##### Description
This is a block in the [`code`](#class-codeclassescode) of a [`screen`](#class-mainscreen)

##### Properties
* rawself: `codeclasses.Base` Just the xml in object form, doesn't serve any purpose
* type: `str` Type of block
* id: `str` Unique id of the block
* x: `int` X position of the block in the editor
* y: `int` Y position of the block in the editor
* statements [`[Statement]`](#class-codeclassesstatement) A list of all statements in the block (if/else/for/etc...)
* next: [`Block`](#class-codeclassesblock) The next block in the code, run after this one
* values [`[Value]`](#class-codeclassesvalue) List of values attached to this block
* top `bool` If this block is at the top of the hierarchy

### *class* codeclasses.**Value**

##### Description
This is a value in the [`code`](#class-codeclassescode) of a [`screen`](#class-mainscreen). It also contains the information for a block, since a value has both

##### Properties
* rawself: `codeclasses.Base` Just the xml in object form, doesn't serve any purpose
* name: `str` Name of the value
* type: `str` Type of block
* id: `str` Unique id of the block
* x: `int` X position of the block in the editor (reserved for top level blocks)
* y: `int` Y position of the block in the editor (reserved for top level blocks)
* statements [`[Statement]`](#class-codeclassesstatement) A list of all statements in the block (if/else/for/etc...)
* next: [`Block`](#class-codeclassesblock) The next block in the code, run after this one
* values [`[Value]`](#class-codeclassesvalue) List of values attached to this block
* top `bool` If this block is at the top of the hierarchy


### *class* codeclasses.**Statement**

##### Description
This is a statement in the [`code`](#class-codeclassescode) of a [`screen`](#class-mainscreen)

##### Properties
* rawself: `codeclasses.Base` Just the xml in object form, doesn't serve any purpose
* name: `str` Name of the statement
* next: [`Block`](#class-block) The next block in the code, run after this statement

### *class* uiclasses.**UI**

##### Description
Represents the screen UI element from a [`screen`](#class-mainscreen)

##### Properties
* rawself: `codeclasses.Base` Just the xml in object form, doesn't serve any purpose
* authURL: `[str]` Authentication for something
* YaVersion: `str` A number for the version of some weird thing named Ya
* Source: `str` Some weird thing
* Properties: [`Properties`](#class-uiclassesproperties) Properties of the screen ui element, everything we want is here, including the list of all the other UI elements

### *class* uiclasses.**Properties**

##### Description
Represents the properties of a screen [`UI`](#class-uiclassesui) element from a [`screen`](#class-mainscreen). Has many more potential properties than shown here, these are just the default ones, if for example the screen's background color is changed, there would be a property to represent that

##### Properties
* rawself: `codeclasses.Base` Just the xml in object form, doesn't serve any purpose
* Name: `str` Name of the screen
* Type: `str` Type of element, can only be "Form"
* Version: `str` I used to believe that App Inventor's code was actually good...
* AppName: `str` Name of the app
* Title: `str` Screen's visible name (the one that shows up in that top bar thing)
* Uuid: `str` A number, the unique id of the screen
* Components: [`[Component]`](#class-uiclassescomponent) A list of all the UI elements in the screen

### *class* uiclasses.**Component**

##### Description
Represents a Component of a screen [`UI`](#class-uiclassesui) element from a [`screen`](#class-mainscreen). Has many more potential properties than shown here, these are just the default ones, if for example the element's background color is changed, there would be a property to represent that

##### Properties
* rawself: `codeclasses.Base` Just the xml in object form, doesn't serve any purpose
* Name: `str` Name of the ui element (IE: "Button1")
* Type: `str` Type of ui element
* Version `str` Why App Inventor? why?
* Uuid: `str` A number, the unique id of the element
* Components: [`[Component]`](#class-uiclassescomponent) A list of all the UI elements in the component (Not always present)


## Custom Parsing

### Explanation
If you have assets that can't be properly parsed just by reading or that aren't images, 
then this might help with your problem. You can use the `parse_function` keyword argument 
when creating a new project to set how every asset will be parsed.

Just create a parsing function, it can be called anything, and do anything as
long as it has three arguments, those being: 
* The project, the object you will modifiy to
add the results from the parsing
* The base asset path, the path to where all the assets are
kept
* The filename, the name of the file inside of the asset path you are currently parsing

#### Example
```python
import parseaia


def myparsefunction(project, assetpath, filename):  # Create a function for parsing
    print(assetpath + filename)  # This one just places all the paths in the assets dictionary

myProject = parseaia.Project("Example.aia", parse_function=myparsefunction)  # Use the function when creating a project
```

