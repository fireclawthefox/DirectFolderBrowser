from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
from DirectFolderBrowser.DirectFolderBrowser import DirectFolderBrowser

from DirectFolderBrowser.DarkTheme import Theme as DarkTheme

loadPrcFileData("", "notify-level info")

app = ShowBase()

def callbackCommand(ok):
    if ok == 1:
        print("User Clicked OK")
        # print the selected file
        print(browser.get())
        browser.hide()
        browser.destroy()
        exit(ok)
    if ok == 0:
        print("User Clicked Cancel")
        browser.hide()
        browser.destroy()
        exit(ok)
# show the browser as file browser
browser = DirectFolderBrowser(
    callbackCommand,
    fileBrowser=True,
    # to enable dark mode, uncomment the folowing line
    #theme=DarkTheme(),
    askForOverwrite=True)

app.run()
