#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

import os
import math
import mimetypes

from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectLabel import DirectLabel
from panda3d.core import (
    LPoint3f,
    TransparencyAttrib,
    TextNode
)
mimetypes.init()

TYPE_POS = 0#350
SIZE_POS = 0#600

def generate(self, content):

    # start position for the folders and files
    xPos = -self.screenWidthPxHalf+32
    zPos = self.screenHeightPxHalf-32


    global TYPE_POS
    TYPE_POS = self.screenWidthPxHalf * 2 - 350
    global SIZE_POS
    SIZE_POS = self.screenWidthPxHalf * 2 - 55

    dirList = []
    fileList = []
    unkList = []

    for entry in content:
        if entry.name.startswith(".") and not self.showHidden:
            continue
        if entry.is_dir():
            dirList.append(entry)
        elif entry.is_file() and self.showFiles:
            if len(self.fileExtensions) > 0:
                if os.path.splitext(entry.name)[1] in self.fileExtensions:
                    fileList.append(entry)
            else:
                fileList.append(entry)
        elif self.showFiles:
            unkList.append(entry)

    def moveNext(entry):
        nonlocal zPos
        if entry.is_dir() or self.showFiles:
            zPos -= 32

    def getKey(item):
        return item.name.lower()

    for entry in sorted(dirList, key=getKey):
        moveNext(entry)
        __createFolder(self, entry, xPos, zPos)
    for entry in sorted(fileList, key=getKey):
        moveNext(entry)
        __createFile(self, entry, xPos, zPos)
    for entry in sorted(unkList, key=getKey):
        moveNext(entry)
        __createUnknown(self, entry, xPos, zPos)

    # recalculate the canvas size
    self.container["canvasSize"] = (-self.screenWidthPxHalf+31, self.screenWidthPxHalf-15, zPos-16, self.screenHeightPxHalf-50)
    self.container.setCanvasSize()

def __createFolder(self, entry, xPos, zPos):
    name = entry.name

    btn = DirectButton(
        parent=self.container.getCanvas(),
        image=f"{self.iconDir}/Folder.png",
        image_scale=16,
        image_pos=(16,0,0),
        relief=1,
        frameColor = (
            (0.9, 0.9, 0.9, 0), # Normal
            (0.95, 0.95, 1, 1), # Click
            (0.9, 0.9, 1, 1), # Hover
            (0.5, 0.5, 0.5, 1)), # Disabled
        frameSize=(0, self.screenWidthPxHalf*2, -16, 16),
        pos=LPoint3f(xPos, 0, zPos),
        text = name,
        text_scale=12,
        text_align=TextNode.ALeft,
        text_pos=(32,-4),
        command=self.folderMoveIn,
        extraArgs=[entry.path]
    )

    lblInfo = __createMIMEInfo(self, btn, entry, True)
    #lblSize = __createSizeInfo(self, btn, entry)

    btn.bind(DGG.MWDOWN, self.scroll, [0.01])
    btn.bind(DGG.MWUP, self.scroll, [-0.01])
    btn.setTransparency(TransparencyAttrib.M_multisample)

def __createFile(self, entry, xPos, zPos):
    name = entry.name
    btn = DirectButton(
        parent=self.container.getCanvas(),
        image=f"{self.iconDir}/File.png",
        image_scale=16,
        image_pos=(16,0,0),
        relief=1,
        frameColor = (
            (0.9, 0.9, 0.9, 0), # Normal
            (0.95, 0.95, 1, 1), # Click
            (0.9, 0.9, 1, 1), # Hover
            (0.5, 0.5, 0.5, 1)), # Disabled
        frameSize=(0, self.screenWidthPxHalf*2, -16, 16),
        pos=LPoint3f(xPos, 0, zPos),
        text = name,
        text_align=TextNode.ALeft,
        text_scale=12,
        text_pos=(32,-4),
        command=self.txtFileName.set,
        extraArgs=[entry.name]
    )

    lblInfo = __createMIMEInfo(self, btn, entry)
    lblSize = __createSizeInfo(self, btn, entry)

    btn.bind(DGG.MWDOWN, self.scroll, [0.01])
    btn.bind(DGG.MWUP, self.scroll, [-0.01])
    btn.setTransparency(TransparencyAttrib.M_multisample)

def __createUnknown(self, entry, xPos, zPos):
    name = entry.name
    lbl = DirectLabel(
        parent=self.container.getCanvas(),
        image=f"{self.iconDir}/File.png",
        image_scale=16,
        image_pos=(16,0,0),
        image_color=(0.9,0.5,0.5,1),
        relief=1,
        frameColor = (0.7, 0.7, 0.7, 0),
        frameSize=(0, self.screenWidthPxHalf*2, -16, 16),
        pos=LPoint3f(xPos, 0, zPos),
        text = name,
        text_align=TextNode.ALeft,
        text_scale=12,
        text_pos=(32,-4),
    )

    lblInfo = __createMIMEInfo(self, lbl, entry)

    lbl.bind(DGG.MWDOWN, self.scroll, [0.01])
    lbl.bind(DGG.MWUP, self.scroll, [-0.01])
    lbl.setTransparency(TransparencyAttrib.M_multisample)

def __createMIMEInfo(self, parent, entry, isFolder=False):
    mimeType = mimetypes.guess_type(entry)
    if isFolder:
        mimeType = "Folder"
    return DirectLabel(
        parent=parent,
        relief=0,
        frameColor = (0, 0, 0, 0),
        frameSize=(0, self.screenWidthPxHalf-TYPE_POS, -16, 16),
        pos=LPoint3f(TYPE_POS, 0, 0),
        text = mimeType,
        text_align=TextNode.ALeft,
        text_scale=12,
        text_pos=(0,-4),
    )

def __createSizeInfo(self, parent, entry, isFolder=False):
    fileSize = getSizeString(os.path.getsize(entry))
    return DirectLabel(
        parent=parent,
        relief=0,
        frameColor = (0, 0, 0, 0),
        frameSize=(0, -150, -16, 16),
        pos=LPoint3f(SIZE_POS, 0, 0),
        text = fileSize,
        text_align=TextNode.ARight,
        text_scale=12,
        text_pos=(0,-4),
    )

def getSizeString(byteSize):
    if byteSize >= pow(10, 24):
        #yotta
        s = pow(10, 24)
        return f"{round(byteSize/s,2)} Yb"
    elif byteSize >= pow(10, 21):
        #zetta
        s = pow(10, 21)
        return f"{round(byteSize/s,2)} Zb"
    elif byteSize >= pow(10, 18):
        #exa
        s = pow(10, 18)
        return f"{round(byteSize/s,2)} Eb"
    elif byteSize >= pow(10, 15):
        #peta
        s = pow(10, 15)
        return f"{round(byteSize/s,2)} Pb"
    elif byteSize >= pow(10, 12):
        #tera
        s = pow(10, 12)
        return f"{round(byteSize/s,2)} Tb"
    elif byteSize >= pow(10, 9):
        #giga
        s = pow(10, 9)
        return f"{round(byteSize/s,2)} Gb"
    elif byteSize >= pow(10, 6):
        #mega
        s = pow(10, 6)
        return f"{round(byteSize/s,2)} Mb"
    elif byteSize >= pow(10, 3):
        #kilo
        s = pow(10, 3)
        return f"{round(byteSize/s,2)} Kb"
    else:
        #bytes
        return f"{byteSize}B"
