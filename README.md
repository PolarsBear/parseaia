# Parse .AIA
This is a simple python library for parsing the contents of .AIA files ([App Inventor](https://appinventor.mit.edu/) Projects).

# Basic Explanation
The library works by extracting all of the data from an app inventor project. The one class you'll need is `parseaia.Project`, it represents one app inventor project.

## Quick Example:
```py
from parseaia import Project

myproj = Project("ExampleApp.aia") # Initiate a Project with the filepath to the .aia

print(myproj.Screen1.UI.Properties.Components) # Printing out all the UI elements
```
This example prints out all the UI elements in the screen "Screen1" (The default screen name when you create an app in app inventor, most apps will have it)

# TODO:
-Extract assets (images/files) as well

-Optimize some code

-Add better classes for a few things

# Documentation
You can find the documentation [HERE](https://parseaia.readthedocs.io/en/latest/)


# Test:

## *class* codeclasses.**Code**
