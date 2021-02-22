
#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

import os

from direct.showbase.DirectObject import DirectObject
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectLabel import DirectLabel
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TransparencyAttrib,
    TextNode,
    Filename
)

from panda3d.core import PGButton, MouseButton
DGG.MWUP = PGButton.getPressPrefix() + MouseButton.wheel_up().getName() + '-'
DGG.MWDOWN = PGButton.getPressPrefix() + MouseButton.wheel_down().getName() + '-'

from .SymbolView import generate as symbolViewGenerate
from .DetailView import generate as detailViewGenerate

VIEWTYPE = {
    "Symbol":symbolViewGenerate,
    "Detail":detailViewGenerate
}

class DirectFolderBrowser(DirectObject):
    def __init__(self, command, fileBrowser=False, defaultPath="~", defaultFilename="unnamed.txt", fileExtensions=[], tooltip=None, iconDir=None, parent=None):
        """
        A simple file and folder browser

        command: The command that will be called on closing the browser
        fileBrowser: If set to True the browser will show files, otherwise it will only show folders
        defaultPath: The initial path the browser will be set to show
        defaultFilename: The filename that will be set by default, only usefull if fileBrowser is True
        fileExtensions: A list of extensions. Only files with those extensions will be shown. Only usefull if fileBrowser is True
        tooltip: An instance of the Tooltip class to display tooltips for certain parts of the editor
        iconDir: A directory path that contains replacement images. It must contain all required images which are:
            File.png
            Folder.png
            FolderNew.png
            FolderShowHidden.png
            FolderUp.png
            Reload.png
        parent: Another DirectGUI element which has pixel2d as root parent.
            The browser frame is placed centered so a frame for example should have equal sizes in horizontal and vertical directions
            e.g. frameSize=(-250,250,-200,200)
        """
        self.tt = tooltip
        self.command = command
        self.showFiles = fileBrowser
        self.fileExtensions = fileExtensions
        self.showHidden = False
        self.parent = parent
        if iconDir is None:
            fn = Filename.fromOsSpecific(os.path.dirname(__file__))
            fn.makeTrueCase()
            self.iconDir = str(fn) + "/icons"
        else:
            self.iconDir = iconDir
        self.selectedViewType = "Symbol"

        self.currentPath = os.path.expanduser(defaultPath)
        if not os.path.exists(self.currentPath):
            self.currentPath = os.path.expanduser("~")
        self.previousPath = self.currentPath

        if self.parent is None:
            self.parent = base.pixel2d
            self.screenWidthPx = base.getSize()[0]
            self.screenHeightPx = base.getSize()[1]
            self.position = LPoint3f(base.getSize()[0]/2, 0, -base.getSize()[1]/2)
        else:
            self.screenWidthPx = self.parent.getWidth()
            self.screenHeightPx = self.parent.getHeight()
            self.position = LPoint3f(0)
        self.screenWidthPxHalf = self.screenWidthPx * 0.5
        self.screenHeightPxHalf = self.screenHeightPx * 0.5

        self.mainFrame = DirectFrame(
            relief=1,
            frameSize=(-self.screenWidthPxHalf,self.screenWidthPxHalf,-self.screenHeightPxHalf,self.screenHeightPxHalf),
            frameColor=(1, 1, 1, 1),
            pos=self.position,
            parent=self.parent,
            state=DGG.NORMAL,
        )

        self.pathRightMargin = 155 # NOTE: Add 28 for each button to the right + 15px margin
        self.pathEntryWidth = self.screenWidthPx - self.pathRightMargin - 28

        # The path entry on top of the window
        self.pathEntry = DirectEntry(
            parent=self.mainFrame,
            relief=DGG.SUNKEN,
            frameColor=(1, 1, 1, 1),
            pad=(0.2, 0.2),
            pos=LPoint3f(-self.screenWidthPxHalf + 15, 0, self.screenHeightPxHalf - 25),
            scale=12,
            width=self.pathEntryWidth/12,
            overflow=True,
            command=self.entryAccept,
            initialText=self.currentPath,
            focusInCommand=base.messenger.send,
            focusInExtraArgs=["unregisterKeyboardEvents"],
            focusOutCommand=base.messenger.send,
            focusOutExtraArgs=["reregisterKeyboardEvents"],
        )

        # ----------------
        # CONTROL BUTTONS
        # ----------------
        x = self.screenWidthPxHalf - self.pathRightMargin + 18

        # RELOAD
        self.btnReload = DirectButton(
            parent=self.mainFrame,
            relief=1,
            frameColor = (
                (0.8, 0.8, 0.8, 1), # Normal
                (0.9, 0.9, 1, 1), # Click
                (0.8, 0.8, 1, 1), # Hover
                (0.5, 0.5, 0.5, 1)), # Disabled
            frameSize=(-14, 14, -10, 18),
            pos=LPoint3f(x, 0, self.screenHeightPxHalf - 25),
            command=self.folderReload,
            image=f"{self.iconDir}/Reload.png",
            image_scale=14,
            image_pos=(0,0,4),
        )
        self.btnReload.setTransparency(TransparencyAttrib.M_multisample)
        if self.tt is not None:
            self.btnReload.bind(DGG.ENTER, self.tt.show, ["Reload Folder"])
            self.btnReload.bind(DGG.EXIT, self.tt.hide)

        # MOVE UP ONE FOLDER
        x += 28
        self.btnFolderUp = DirectButton(
            parent=self.mainFrame,
            relief=1,
            frameColor = (
                (0.8, 0.8, 0.8, 1), # Normal
                (0.9, 0.9, 1, 1), # Click
                (0.8, 0.8, 1, 1), # Hover
                (0.5, 0.5, 0.5, 1)), # Disabled
            frameSize=(-14, 14, -10, 18),
            pos=LPoint3f(x, 0, self.screenHeightPxHalf - 25),
            command=self.folderUp,
            image=f"{self.iconDir}/FolderUp.png",
            image_scale=14,
            image_pos=(0,0,4),
        )
        self.btnFolderUp.setTransparency(TransparencyAttrib.M_multisample)
        if self.tt is not None:
            self.btnFolderUp.bind(DGG.ENTER, self.tt.show, ["Move up one level"])
            self.btnFolderUp.bind(DGG.EXIT, self.tt.hide)

        # CREATE NEW FOLDER
        x += 28
        self.btnFolderNew = DirectButton(
            parent=self.mainFrame,
            relief=1,
            frameColor = (
                (0.8, 0.8, 0.8, 1), # Normal
                (0.9, 0.9, 1, 1), # Click
                (0.8, 0.8, 1, 1), # Hover
                (0.5, 0.5, 0.5, 1)), # Disabled
            frameSize=(-14, 14, -10, 18),
            pos=LPoint3f(x, 0, self.screenHeightPxHalf - 25),
            command=self.folderNew,
            image=f"{self.iconDir}/FolderNew.png",
            image_scale=14,
            image_pos=(0,0,4),
        )
        self.btnFolderNew.setTransparency(TransparencyAttrib.M_multisample)
        if self.tt is not None:
            self.btnFolderNew.bind(DGG.ENTER, self.tt.show, ["Create new folder"])
            self.btnFolderNew.bind(DGG.EXIT, self.tt.hide)

        # SHOW HIDDEN FOLDERS
        x += 28
        self.btnFolderShowHidden = DirectButton(
            parent=self.mainFrame,
            relief=1,
            frameColor = (
                (0.8, 0.8, 0.8, 1), # Normal
                (0.9, 0.9, 1, 1), # Click
                (0.8, 0.8, 1, 1), # Hover
                (0.5, 0.5, 0.5, 1)), # Disabled
            frameSize=(-14, 14, -10, 18),
            pos=LPoint3f(x, 0, self.screenHeightPxHalf - 25),
            command=self.folderShowHidden,
            image=f"{self.iconDir}/FolderShowHidden.png",
            image_scale=14,
            image_pos=(0,0,4),
        )
        self.btnFolderShowHidden.setTransparency(TransparencyAttrib.M_multisample)
        if self.tt is not None:
            self.btnFolderShowHidden.bind(DGG.ENTER, self.tt.show, ["Show/Hide hidden files and folders"])
            self.btnFolderShowHidden.bind(DGG.EXIT, self.tt.hide)

        # TOGGLE VIEW TYPE
        x += 28
        self.btnViewType = DirectButton(
            parent=self.mainFrame,
            relief=1,
            frameColor = (
                (0.8, 0.8, 0.8, 1), # Normal
                (0.9, 0.9, 1, 1), # Click
                (0.8, 0.8, 1, 1), # Hover
                (0.5, 0.5, 0.5, 1)), # Disabled
            frameSize=(-14, 14, -10, 18),
            pos=LPoint3f(x, 0, self.screenHeightPxHalf - 25),
            command=self.toggleViewType,
            image=f"{self.iconDir}/ViewTypeSymbol.png",
            image_scale=14,
            image_pos=(0,0,4),
        )
        self.btnViewType.setTransparency(TransparencyAttrib.M_multisample)
        if self.tt is not None:
            self.btnViewType.bind(DGG.ENTER, self.tt.show, ["Toggle view between Symbols and Detail list"])
            self.btnViewType.bind(DGG.EXIT, self.tt.hide)

        # --------------
        # CONTENT FRAME
        # --------------
        color = (
            (0.8, 0.8, 0.8, 1), # Normal
            (0.9, 0.9, 1, 1), # Click
            (0.8, 0.8, 1, 1), # Hover
            (0.5, 0.5, 0.5, 1)) # Disabled
        self.container = DirectScrolledFrame(
            relief=DGG.RIDGE,
            borderWidth=(2, 2),
            frameColor=(1, 1, 1, 1),
            frameSize=(-self.screenWidthPxHalf+10, self.screenWidthPxHalf-10, -self.screenHeightPxHalf+50, self.screenHeightPxHalf-50),
            canvasSize=(-self.screenWidthPxHalf+31, self.screenWidthPxHalf-10, -self.screenHeightPxHalf+50, self.screenHeightPxHalf-50),
            pos=LPoint3f(0, 0, 0),
            parent=self.mainFrame,
            scrollBarWidth=20,
            verticalScroll_scrollSize=20,
            verticalScroll_thumb_relief=DGG.FLAT,
            verticalScroll_incButton_relief=DGG.FLAT,
            verticalScroll_decButton_relief=DGG.FLAT,
            verticalScroll_thumb_frameColor=color,
            verticalScroll_incButton_frameColor=color,
            verticalScroll_decButton_frameColor=color,
            horizontalScroll_thumb_relief=DGG.FLAT,
            horizontalScroll_incButton_relief=DGG.FLAT,
            horizontalScroll_decButton_relief=DGG.FLAT,
            horizontalScroll_thumb_frameColor=color,
            horizontalScroll_incButton_frameColor=color,
            horizontalScroll_decButton_frameColor=color,
            state=DGG.NORMAL,
        )
        self.container.bind(DGG.MWDOWN, self.scroll, [0.01])
        self.container.bind(DGG.MWUP, self.scroll, [-0.01])

        # ACCEPT BUTTON
        self.btnOk = DirectButton(
            parent=self.mainFrame,
            relief=1,
            frameColor = (
                (0.8, 0.8, 0.8, 1), # Normal
                (0.9, 0.9, 1, 1), # Click
                (0.8, 0.8, 1, 1), # Hover
                (0.5, 0.5, 0.5, 1)), # Disabled
            frameSize=(-45, 45, -6, 14),
            pos=LPoint3f(self.screenWidthPxHalf-160, 0, -self.screenHeightPxHalf+25),
            text = "ok",
            text_scale=12,
            command=command,
            extraArgs=[1],
        )

        # CANCEL BUTTON
        self.btnCancel = DirectButton(
            parent=self.mainFrame,
            relief=1,
            frameColor = (
                (0.8, 0.8, 0.8, 1), # Normal
                (0.9, 0.9, 1, 1), # Click
                (0.8, 0.8, 1, 1), # Hover
                (0.5, 0.5, 0.5, 1)), # Disabled
            frameSize=(-45, 45, -6, 14),
            pos=LPoint3f(self.screenWidthPxHalf-55, 0, -self.screenHeightPxHalf+25),
            text = "Cancel",
            text_scale=12,
            command=command,
            extraArgs=[0]
        )

        # SELECTED FILE ENTRY FIELD
        if self.showFiles:
            self.txtFileName = DirectEntry(
                parent=self.mainFrame,
                relief=DGG.SUNKEN,
                frameColor=(1, 1, 1, 1),
                pad=(0.2, 0.2),
                pos=LPoint3f(-self.screenWidthPxHalf+25, 0, -self.screenHeightPxHalf+25),
                scale=12,
                width=200/12,
                overflow=True,
                command=self.filenameAccept,
                initialText=defaultFilename,
                focusInCommand=base.messenger.send,
                focusInExtraArgs=["unregisterKeyboardEvents"],
                focusOutCommand=base.messenger.send,
                focusOutExtraArgs=["reregisterKeyboardEvents"],
            )

        # ------------------
        # CREATE NEW FOLDER
        # ------------------
        # FRAME FOR CREATING NEW FOLDER
        self.newFolderFrame = DirectFrame(
            parent=self.mainFrame,
            relief=1,
            frameSize=(-self.screenWidthPxHalf+10,self.screenWidthPxHalf-10,-20,20),
            pos=LPoint3f(0, 0, self.screenHeightPxHalf-55),
            frameColor=(0.5,0.5,0.5,1),
        )

        # LABEL FOR NEW FOLDER NAME ENTRY
        self.txtNewFolderName = DirectLabel(
            parent=self.newFolderFrame,
            text="New Folder Name",
            text_scale=12,
            frameColor=(0,0,0,0),
            text_align=TextNode.ALeft,
            pos=(-self.screenWidthPxHalf+15, 0, -3),
        )

        # ENTRY FOR THE NEW FOLDER NAME
        self.folderName = DirectEntry(
            parent=self.newFolderFrame,
            relief=DGG.SUNKEN,
            frameColor=(1, 1, 1, 1),
            pad=(0.2, 0.2),
            pos=LPoint3f(-self.screenWidthPxHalf+25 + self.txtNewFolderName.getWidth(), 0, -4),
            scale=12,
            width=((self.screenWidthPxHalf-25)*2-self.txtNewFolderName.getWidth() - 100)/12,
            overflow=True,
            command=self.entryAccept,
            initialText="New Folder",
            focusInCommand=base.messenger.send,
            focusInExtraArgs=["unregisterKeyboardEvents"],
            focusOutCommand=base.messenger.send,
            focusOutExtraArgs=["reregisterKeyboardEvents"],
        )

        # ACCEPT BUTTON FOR THE CREATE NEW FOLDER
        self.btnCreate = DirectButton(
            parent=self.newFolderFrame,
            relief=1,
            frameColor = (
                (0.8, 0.8, 0.8, 1), # Normal
                (0.9, 0.9, 1, 1), # Click
                (0.8, 0.8, 1, 1), # Hover
                (0.5, 0.5, 0.5, 1)), # Disabled
            frameSize=(-45, 45, -6, 14),
            pos=LPoint3f(self.screenWidthPxHalf-65, 0, -4),
            text = "Create",
            text_scale=12,
            command=self.folderCreate,
            extraArgs=[0]
        )
        # Hide the create new folder frame by default
        self.newFolderFrame.hide()

        # ---------------
        # UPDATE CONTENT
        # ---------------
        # Initial loading of the files and folders of the current path
        self.folderReload()

        # handle window resizing
        self.prevScreenSize = base.getSize()
        if self.parent is base.pixel2d:
            self.accept("window-event", self.windowEventHandler)

    def show(self):
        self.mainFrame.show()
        if self.parent is None:
            self.accept("window-event", self.windowEventHandler)

    def hide(self):
        self.ignore("window-event")
        self.mainFrame.hide()

    def destroy(self):
        self.ignore("window-event")
        self.mainFrame.destroy()

    def scroll(self, scrollStep, event):
        self.container.verticalScroll.scrollStep(scrollStep)

    def get(self):
        if self.showFiles:
            return os.path.join(self.currentPath, self.txtFileName.get(True))
        return self.currentPath

    def filenameAccept(self, filename):
        self.command(1)

    def entryAccept(self, path):
        self.folderReload()

    def folderReload(self):

        for element in self.container.getCanvas().getChildren():
            element.removeNode()

        path = self.pathEntry.get(True)
        path = os.path.expanduser(path)
        path = os.path.expandvars(path)
        if not os.path.exists(path): return
        self.currentPath = path

        try:
            content = os.scandir(path)
        except PermissionError:
            base.messenger.send("showWarning", ["Access denied!"])
            self.pathEntry.set(self.previousPath)
            self.currentPath = self.previousPath
            self.folderReload()
            return

        # start position for the folders and files
        VIEWTYPE[self.selectedViewType](self, content)

    def folderUp(self):
        self.previousPath = self.currentPath
        self.currentPath = os.path.normpath(os.path.join(self.currentPath, ".."))
        self.pathEntry.set(self.currentPath)
        self.folderReload()

    def folderMoveIn(self, path):
        path = os.path.expanduser(path)
        path = os.path.expandvars(path)
        self.previousPath = self.currentPath
        self.currentPath = path
        self.pathEntry.set(path)
        self.folderReload()
        self.container.verticalScroll["value"] = 0

    def folderNew(self):
        if self.newFolderFrame.isHidden():
            self.newFolderFrame.show()
        else:
            self.newFolderFrame.hide()

    def folderShowHidden(self):
        self.showHidden = not self.showHidden
        self.folderReload()

    def toggleViewType(self):
        if self.selectedViewType == "Symbol":
            self.selectedViewType = "Detail"
            self.btnViewType["image"] = f"{self.iconDir}/ViewTypeDetail.png"
        else:
            self.selectedViewType = "Symbol"
            self.btnViewType["image"] = f"{self.iconDir}/ViewTypeSymbol.png"

        self.folderReload()

    def folderCreate(self, path=""):
        try:
            os.makedirs(os.path.join(self.currentPath, self.folderName.get(True)))
        except:
            base.messenger.send("showWarning", ["Can't create folder"])
        self.newFolderFrame.hide()
        self.folderReload()

    def windowEventHandler(self, window=None):
        if window != base.win:
            # This event isn't about our window.
            return


        if window is not None: # window is none if panda3d is not started
            if self.prevScreenSize == base.getSize():
                return
            self.prevScreenSize = base.getSize()
            self.screenWidthPx = base.getSize()[0]
            self.screenWidthPxHalf = self.screenWidthPx * 0.5
            self.screenHeightPx = base.getSize()[1]
            self.screenHeightPxHalf = self.screenHeightPx * 0.5

            # reposition and resize all gui elements
            self.mainFrame.setPos(self.screenWidthPx/2, 0, -self.screenHeightPx/2)
            self.mainFrame["frameSize"] = (-self.screenWidthPxHalf,self.screenWidthPxHalf,-self.screenHeightPxHalf,self.screenHeightPxHalf)

            self.pathEntryWidth = self.screenWidthPx - self.pathRightMargin - 28
            self.pathEntry.setPos(LPoint3f(-self.screenWidthPxHalf + 15, 0, self.screenHeightPxHalf - 25))
            self.pathEntry["width"] = self.pathEntryWidth/12
            self.pathEntry.resetFrameSize()

            # reposition top right icons
            x = self.screenWidthPxHalf - self.pathRightMargin + 14
            self.btnReload.setPos(LPoint3f(x, 0, self.screenHeightPxHalf - 25))
            x += 28
            self.btnFolderUp.setPos(pos=LPoint3f(x, 0, self.screenHeightPxHalf - 25))
            x += 28
            self.btnFolderNew.setPos(pos=LPoint3f(x, 0, self.screenHeightPxHalf - 25))
            x += 28
            self.btnFolderShowHidden.setPos(pos=LPoint3f(x, 0, self.screenHeightPxHalf - 25))
            x += 28
            self.btnViewType.setPos(pos=LPoint3f(x, 0, self.screenHeightPxHalf - 25))

            # resize the browsing area
            self.container["frameSize"] = (-self.screenWidthPxHalf+10, self.screenWidthPxHalf-10, -self.screenHeightPxHalf+50, self.screenHeightPxHalf-50)
            # Note: canvas size of the container will be reset in the
            #       folder Reload call at the end of this function
            self.btnOk.setPos(LPoint3f(self.screenWidthPxHalf-160, 0, -self.screenHeightPxHalf+25))
            self.btnCancel.setPos(LPoint3f(self.screenWidthPxHalf-55, 0, -self.screenHeightPxHalf+25))
            if self.showFiles:
                self.txtFileName.setPos(LPoint3f(-self.screenWidthPxHalf+25, 0, -self.screenHeightPxHalf+25))
            self.newFolderFrame.setPos(LPoint3f(0, 0, self.screenHeightPxHalf-55))
            self.newFolderFrame["frameSize"] = (-self.screenWidthPxHalf+10,self.screenWidthPxHalf-10,-20,20)
            self.txtNewFolderName.setPos(-self.screenWidthPxHalf+15, 0, -3)
            self.folderName.setPos(LPoint3f(-self.screenWidthPxHalf+25 + self.txtNewFolderName.getWidth(), 0, -4))
            self.folderName["width"]=((self.screenWidthPxHalf-25)*2-self.txtNewFolderName.getWidth() - 100)/12
            self.btnCreate.setPos(LPoint3f(self.screenWidthPxHalf-65, 0, -4))

            self.folderReload()
