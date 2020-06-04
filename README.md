# DirectFolderBrowser
A file and folder browser for Panda3D using DirectGUI

## Features
This is a simple fullscreen file and folder browser with a basic featureset. Currently implemented are:

- Browsing files and folders
- Show/Hide hidden files (using unix like leading dot)
- Create new folders
- Filter by file extension
- Resizes with window size changes

## How to use
```
from DirectFolderBrowser import DirectFolderBrowser

# this command will be called by the browser
def callbackCommand(ok):
    if ok == 1:
        print("User Clicked OK")
        
        # print the selected file
        print(browser.get())
        
        browser.hide()
        # Destroy the browser if it's not needed anymore
        #browser.destroy()
    elif ok == 0:
        print("User Clicked Cancel")
        browser.hide()
        browser.destroy()

# show the browser as file browser
browser = DirectFolderBrowser(callbackCommand, fileBrowser=True)
```
