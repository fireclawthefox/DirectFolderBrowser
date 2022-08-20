#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

import math, os

from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectLabel import DirectLabel
from panda3d.core import (
    LPoint3f,
    TransparencyAttrib
)


def generate(self, content, selected):

    # start position for the folders and files
    xPos = -self.screenWidthPxHalf + 20 + 50 - 110
    zPos = self.screenHeightPxHalf-60-40

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
        nonlocal xPos
        nonlocal zPos
        if entry.is_dir() or self.showFiles:
            if xPos + 110 > self.screenWidthPxHalf - 45:
                # move to the next line if we hit the right border (incl. scrollbar size)
                xPos = -self.screenWidthPxHalf + 20 + 50
                zPos -= 110
            else:
                # move right the next position
                xPos += 110

    def getKey(item):
        return item.name.lower()

    for entry in sorted(dirList, key=getKey):
        moveNext(entry)
        btn = __createFolder(self, entry, xPos, zPos)
        if selected == entry.name:
            btn["frameColor"] = self.theme.selected_background
    for entry in sorted(fileList, key=getKey):
        moveNext(entry)
        btn = __createFile(self, entry, xPos, zPos)
        if selected == entry.name:
            btn["frameColor"] = self.theme.selected_background
    for entry in sorted(unkList, key=getKey):
        moveNext(entry)
        __createUnknown(self, entry.name, xPos, zPos)

    # recalculate the canvas size
    self.container["canvasSize"] = (-self.screenWidthPxHalf+31, self.screenWidthPxHalf-15, zPos-90, self.screenHeightPxHalf-50)
    self.container.setCanvasSize()

def __createFolder(self, entry, xPos, zPos):
    name = entry.name
    if len(entry.name) > 10:
        name = ""
        for i in range(max(math.ceil(len(entry.name)/10), 4)):
            name += entry.name[i*10:i*10+10]+"\n"
        name = name[:-1]
        if math.ceil(len(entry.name)/10) > 4:
            name += "..."
    btn = DirectButton(
        parent=self.container.getCanvas(),
        image=loader.load_texture(f"{self.iconDir}/Folder.png", loaderOptions=self.imageOpts),
        image_scale=35,
        relief=1,
        frameColor = self.theme.folder_background,
        frameSize=(-40, 40, -40, 40),
        pos=LPoint3f(xPos, 0, zPos),
        text = name,
        text_scale=12,
        text_pos=(0,-40),
        text_fg=self.theme.default_text_color,
        command=self.folderClick,
    )
    btn["extraArgs"] = [name, entry.path, btn]
    btn.bind(DGG.MWDOWN, self.scroll, [0.01])
    btn.bind(DGG.MWUP, self.scroll, [-0.01])
    btn.setTransparency(TransparencyAttrib.M_multisample)
    return btn

def __createFile(self, entry, xPos, zPos):
    filename = entry.name
    name = filename
    if len(filename) > 10:
        name = ""
        for i in range(min(math.ceil(len(filename)/10), 4)):
            name += filename[i*10:i*10+10]+"\n"
        name = name[:-1]
        if math.ceil(len(filename)/10) > 4:
            name += "..."
    btn = DirectButton(
        parent=self.container.getCanvas(),
        image=loader.load_texture(f"{self.iconDir}/File.png", loaderOptions=self.imageOpts),
        image_scale=35,
        relief=1,
        frameColor = self.theme.file_background,
        frameSize=(-40, 40, -40, 40),
        pos=LPoint3f(xPos, 0, zPos),
        text = name,
        text_scale=12,
        text_pos=(0,-40),
        text_fg=self.theme.default_text_color,
        command=self.fileClick,
    )
    btn["extraArgs"] = [filename, entry.path, btn]
    btn.bind(DGG.MWDOWN, self.scroll, [0.01])
    btn.bind(DGG.MWUP, self.scroll, [-0.01])
    btn.setTransparency(TransparencyAttrib.M_multisample)
    return btn

def __createUnknown(self, filename, xPos, zPos):
    name = filename
    if len(filename) > 10:
        name = ""
        for i in range(math.ceil(len(filename)/10)):
            name += filename[i*10:i*10+10]+"\n"
        name = name[:-1]
    lbl = DirectLabel(
        parent=self.container.getCanvas(),
        image=loader.load_texture(f"{self.iconDir}/File.png", loaderOptions=self.imageOpts),
        image_scale=35,
        image_color=self.theme.unknown_image_tint,
        relief=1,
        frameColor = (0.7, 0.7, 0.7, 0),
        frameSize=(-40, 40, -40, 40),
        pos=LPoint3f(xPos, 0, zPos),
        text = name,
        text_scale=12,
        text_pos=(0,-40),
        text_fg=self.theme.default_text_color,
    )
    lbl.bind(DGG.MWDOWN, self.scroll, [0.01])
    lbl.bind(DGG.MWUP, self.scroll, [-0.01])
    lbl.setTransparency(TransparencyAttrib.M_multisample)

