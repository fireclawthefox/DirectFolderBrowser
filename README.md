# DirectFolderBrowser
A file and folder browser for Panda3D using DirectGUI

## Features
This is a simple fullscreen file and folder browser with a basic featureset. Currently implemented are:

- Browsing files and folders
- Display content as symbols or in a detailed list
- Show/Hide hidden files (using unix like leading dot)
- Create new folders
- Filter by file extension
- Resizes with window size changes
- Makes use of the <a href="https://github.com/fireclawthefox/DirectTooltip">Tooltip class</a>

## Install
Install the DirectFolderBrowser via pip

```bash
pip install DirectFolderBrowser
```

## How to use
To add a browser instance to your running Panda3D application, just instantiate it like shown here:
```python3
from DirectFolderBrowser.DirectFolderBrowser import DirectFolderBrowser

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

### Parameters
The DirectFolderBrowser accepts a few arguments.
- <b>command:</b> The command that will be called on closing the browser
- <b>fileBrowser:</b> If set to True the browser will show files, otherwise it will only show folders
- <b>defaultPath:</b> The initial path the browser will be set to show
- <b>defaultFilename:</b> The filename that will be set by default, <i>only usefull if fileBrowser is True</i>
- <b>fileExtensions:</b> A list of extensions. Only files with those extensions will be shown. <i>Only usefull if fileBrowser is True</i>
- <b>tooltip:</b> An instance of the <a href="https://github.com/fireclawthefox/DirectTooltip">Tooltip class</a> to display tooltips for certain parts of the editor
- <b>iconDir:</b> A directory path that contains replacement images. It must contain all required images which are:<br />
    File.png<br />
    Folder.png<br />
    FolderNew.png<br />
    FolderShowHidden.png<br />
    FolderUp.png<br />
    Reload.png<br />
- <b>parent:</b> Another DirectGUI element which has pixel2d as root parent.<br />
    The browser frame is placed centered so a frame for example should have equal sizes in horizontal and vertical directions<br />
    e.g. frameSize=(-250,250,-200,200)<br />
