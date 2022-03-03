# Parse .AIA
This is a python library for extracting code, UI data, images and assets from .AIA files ([App Inventor](https://appinventor.mit.edu/) Projects).

# Basic Explanation
The library works by extracting all of the data from an app inventor project. The one class you'll need is `parseaia.Project`, it represents one app inventor project.

## Quick Example:
```py
from parseaia import Project

myproj = Project("ExampleApp.aia") # Initiate a Project with the filepath to the .aia

print(myproj.Screen1.UI.Properties.Components) # Printing out all the UI elements
```
This example prints out all the UI elements in the screen "Screen1" (The default screen name when you create an app in app inventor, most apps will have it)

# GUI
There is also an inspector GUI for exploring app inventor projects

You'll need PyQt5 to run it:
`pip install PyQt5`

Then you can run:
`python -m parseaia`

To open a file, just press File>Open and then select the .aia you want to open

# TODO

- Add some more error catching
- Add support for video files

# Known issues
- `__main__` Does not support audio files

# Links
- [Documentation](https://parseaia.readthedocs.io/en/latest/)
- [PyPI](https://pypi.org/project/parseaia/)
