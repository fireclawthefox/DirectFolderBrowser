from direct.showbase.ShowBase import ShowBase
from DirectFolderBrowser.DirectFolderBrowser import DirectFolderBrowser

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
browser = DirectFolderBrowser(callbackCommand, fileBrowser=True)

app.run()
